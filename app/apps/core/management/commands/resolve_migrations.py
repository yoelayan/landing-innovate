import subprocess
import sys
from django.core.management.base import BaseCommand
from django.db.migrations.executor import MigrationExecutor
from django.db import connections, DEFAULT_DB_ALIAS

class Command(BaseCommand):
    help = 'Detect and resolve conflicting migrations'

    def add_arguments(self, parser):
        parser.add_argument(
            '--database',
            default=DEFAULT_DB_ALIAS,
            help='Nominates a database to check migrations for',
        )
        parser.add_argument(
            '--noinput', '--no-input',
            action='store_false', dest='interactive', default=True,
            help='Do not prompt the user for input of any kind.',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Checking migrations..."))
        
        # Check for conflict using migrate --plan
        try:
            result = subprocess.run(
                ['python', 'manage.py', 'migrate', '--plan'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if "CONFLICT" in result.stdout or "CONFLICT" in result.stderr:
                self.stdout.write(self.style.WARNING(
                    "Conflicting migrations detected. Attempting to merge..."
                ))
                
                # Run makemigrations --merge
                merge_cmd = ['python', 'manage.py', 'makemigrations', '--merge']
                if not options['interactive']:
                    merge_cmd.append('--noinput')
                    
                merge_result = subprocess.run(
                    merge_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                if merge_result.returncode == 0:
                    self.stdout.write(self.style.SUCCESS(
                        "Successfully merged conflicting migrations."
                    ))
                    self.stdout.write(merge_result.stdout)
                else:
                    self.stdout.write(self.style.ERROR(
                        "Failed to merge migrations automatically."
                    ))
                    self.stdout.write(merge_result.stderr)
                    return
            else:
                self.stdout.write(self.style.SUCCESS("No migration conflicts detected."))
                
            # After resolving conflicts (or if no conflicts), run migrate
            self.stdout.write(self.style.NOTICE("Applying migrations..."))
            migrate_result = subprocess.run(
                ['python', 'manage.py', 'migrate'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            if migrate_result.returncode == 0:
                self.stdout.write(self.style.SUCCESS("Migrations applied successfully."))
            else:
                self.stdout.write(self.style.ERROR("Failed to apply migrations."))
                self.stdout.write(migrate_result.stderr)
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error checking migrations: {str(e)}"))
            return 