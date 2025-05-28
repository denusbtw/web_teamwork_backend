import factory
from faker import Faker
from django.utils import timezone

from ..models import User

faker = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    date_joined = factory.LazyFunction(
        lambda: timezone.make_aware(faker.date_time_this_year())
    )
    is_active = True
    role = factory.Faker("random_element", elements=[c[0] for c in User.Role.choices])

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        password = (
            extracted
            if extracted
            else factory.Faker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).evaluate(None, None, extra={"locale": None})
        )
        self.set_password(password)

    class Meta:
        model = User
        skip_postgeneration_save = True
