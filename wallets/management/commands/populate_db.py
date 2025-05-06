import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from accounts.models import User
from wallets.models import Wallet, Transaction


class Command(BaseCommand):
    help = 'Popula o banco de dados com dados fictícios para demonstração'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=10,
            help='Número de usuários a serem criados'
        )
        parser.add_argument(
            '--transactions',
            type=int,
            default=50,
            help='Número total de transações a serem criadas'
        )

    def handle(self, *args, **options):
        fake = Faker('pt_BR')

        if User.objects.exists():
            self.stdout.write(self.style.WARNING(
                'O banco de dados já contém dados. Abortando...'
            ))
            return

        num_users = options['users']
        num_txs = options['transactions']

        with transaction.atomic():
            # 1) Cria superusuário
            admin = User.objects.create_superuser(
                email='admin@example.com',
                password='Dev.1234',
                first_name='Admin',
                last_name='Sistema'
            )
            Wallet.objects.create(user=admin, balance=Decimal('10000.00'))
            self.stdout.write(self.style.SUCCESS(
                'Superusuário criado: admin@example.com (senha: Dev.1234)'
            ))

            # 2) Cria usuários normais e carteiras
            wallets = []
            for _ in range(num_users):
                user = User.objects.create_user(
                    email=fake.unique.email(),
                    password='senha123',
                    first_name=fake.first_name(),
                    last_name=fake.last_name()
                )
                wallet = Wallet.objects.create(
                    user=user,
                    balance=Decimal(random.uniform(1000, 10000)).quantize(Decimal('0.00'))
                )
                wallets.append(wallet)
                self.stdout.write(f'Usuário criado: {user.email} (saldo: {wallet.balance})')

            # 3) Cria transações com status aleatório
            STATUS_CHOICES = ['completed', 'pending', 'failed']
            for i in range(num_txs):
                sender, receiver = random.sample(wallets, 2)
                max_amount = float(sender.balance)
                # garantia de mínimo 0.01
                amount = Decimal(random.uniform(0.01, max_amount or 0.01)).quantize(Decimal('0.00'))

                status = random.choices(
                    STATUS_CHOICES,
                    weights=[0.7, 0.2, 0.1],  # 70% concluídas, 20% pendentes, 10% falhas
                    k=1
                )[0]

                tx = Transaction.objects.create(
                    sender_wallet=sender,
                    receiver_wallet=receiver,
                    amount=amount,
                    status=status,
                    note=fake.sentence()
                )

                # Apenas para transações concluídas, atualiza saldos
                if status == 'completed':
                    sender.balance -= amount
                    receiver.balance += amount
                    sender.save()
                    receiver.save()
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'[{i + 1}/{num_txs}] Tx#{tx.id}:'
                            f'{status.upper()} R${amount} de {sender.user.email} para {receiver.user.email}'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f'[{i + 1}/{num_txs}] Tx#{tx.id}: {status.upper()}'
                            f'R${amount} de {sender.user.email} para {receiver.user.email}'
                        )
                    )

            self.stdout.write(self.style.SUCCESS(
                f'Banco populado com {num_users} usuários e {num_txs} transações!'
            ))
