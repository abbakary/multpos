from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction

from tracker.models import Order


class Command(BaseCommand):
    help = "Auto-progress orders from 'created' to 'in_progress' after 10 minutes."

    def add_arguments(self, parser):
        parser.add_argument(
            "--minutes",
            type=int,
            default=10,
            help="Age (in minutes) after which 'created' orders should progress to 'in_progress' (default: 10)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Do not write changes, only report what would be updated",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=500,
            help="Max number of orders to process in this run (default: 500)",
        )

    def handle(self, *args, **options):
        minutes = options["minutes"]
        dry_run = options["dry_run"]
        limit = options["limit"]

        cutoff = timezone.now() - timezone.timedelta(minutes=minutes)

        qs = (
            Order.objects.filter(status="created", created_at__lte=cutoff)
            .order_by("created_at")
        )
        total_candidates = qs.count()
        to_process = list(qs[:limit].values_list("id", flat=True))

        if not to_process:
            self.stdout.write(self.style.SUCCESS(f"No orders eligible for auto progression (checked {total_candidates})."))
            return

        self.stdout.write(f"Eligible orders: {total_candidates}. Processing up to {len(to_process)}…")

        now = timezone.now()
        updated = 0

        # Process in small batches to avoid long transactions
        batch_size = 100
        for i in range(0, len(to_process), batch_size):
            batch_ids = to_process[i : i + batch_size]
            if dry_run:
                # Simulate
                updated += len(batch_ids)
                continue
            with transaction.atomic():
                # Set status and started_at if not set
                rows = (
                    Order.objects.filter(id__in=batch_ids, status="created")
                    .update(status="in_progress", started_at=now)
                )
                updated += rows

        msg = f"Auto-progressed {updated} order(s) to in_progress."
        if dry_run:
            msg = "[DRY RUN] " + msg
        self.stdout.write(self.style.SUCCESS(msg))
