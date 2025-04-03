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

    def handle(self, *args, **options):
        fake = Faker('pt_BR')

        if User.objects.exists():
            self.stdout.write(self.style.WARNING('O banco de dados já contém dados. Abortando...'))
            return

        with transaction.atomic():
            # Cria superusuário
            admin = User.objects.create_superuser(
                email='admin@example.com',
                password='Dev.1234',
                first_name='Admin',
                last_name='Sistema'
            )
            Wallet.objects.create(user=admin, balance=Decimal('10000.00'))
            self.stdout.write(self.style.SUCCESS('Superusuário criado: admin@example.com (senha: Dev.1234)'))

            # Cria usuários normais
            num_users = options['users']
            for _ in range(num_users):
                user_data = {
                    'email': fake.unique.email(),
                    'password': 'senha123',
                    'first_name': fake.first_name(),
                    'last_name': fake.last_name(),
                }
                user = User.objects.create_user(**user_data)

                # Cria carteira com saldo aleatório
                Wallet.objects.create(
                    user=user,
                    balance=Decimal(random.uniform(1000, 10000)).quantize(Decimal('0.00'))
                )
                self.stdout.write(f'Usuário criado: {user.email}')

            # Cria transações entre carteiras
            wallets = list(Wallet.objects.all())
            for _ in range(50):
                sender, receiver = random.sample(wallets, 2)

                # Garante que o valor não exceda o saldo
                max_amount = float(sender.balance)
                amount = Decimal(random.uniform(10.0, max_amount)).quantize(Decimal('0.00'))

                Transaction.objects.create(
                    sender_wallet=sender,
                    receiver_wallet=receiver,
                    amount=amount,
                    status='completed',
                    note=fake.sentence()
                )

                # Atualiza saldos
                sender.balance -= amount
                receiver.balance += amount
                sender.save()
                receiver.save()

            self.stdout.write(self.style.SUCCESS(f'Banco de dados populado com {num_users} usuários e 50 transações!'))
