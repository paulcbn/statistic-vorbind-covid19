from django.db import models

from api_core.config.counties import Counties


class DataSource(models.Model):
    class Meta:
        verbose_name = 'Sursă de date'
        verbose_name_plural = 'Surse de date'

    url = models.URLField(verbose_name="Sursa de informare", unique=True)
    parsed_content = models.TextField(verbose_name="Continutul parsat")
    title = models.TextField(verbose_name="Titlul articolului")

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Momentul crearii sursei")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Momentul ultimei modificari")

    def __str__(self):
        return self.url


class Comorbidity(models.Model):
    class Meta:
        verbose_name = 'Comorbiditate'
        verbose_name_plural = 'Comorbidități'

    name = models.CharField(verbose_name="Numele conditiei medicale", max_length=200, unique=True)

    def __str__(self):
        return self.name


class Hospital(models.Model):
    class Meta:
        verbose_name = 'Spital'
        verbose_name_plural = 'Spitale'

    name = models.CharField(verbose_name="Numele spitalului", max_length=200, unique=True)

    def __str__(self):
        return self.name


class Case(models.Model):
    class Meta:
        unique_together = ['case_number', 'collision_index']
        verbose_name = 'Caz'
        verbose_name_plural = 'Cazuri'

    case_number = models.PositiveIntegerField(verbose_name="Numarul cazului")
    collision_index = models.PositiveIntegerField(
        verbose_name="Indice suprapunere")

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Momentul crearii cazului")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Momentul ultimei modificari")

    MALE = 'M'
    FEMALE = 'F'

    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Sex", null=True, blank=True)
    age = models.PositiveSmallIntegerField(verbose_name="Varsta", null=True, blank=True)
    county = models.CharField(max_length=2, choices=Counties.CHOICES, verbose_name="Judet", null=True, blank=True)

    hospital_admission_date = models.DateField(verbose_name="Data internarii", null=True, blank=True)
    test_date = models.DateField(verbose_name="Data recoltarii probei", null=True, blank=True)
    positive_result_date = models.DateField(verbose_name="Data rezultatului pozitiv", null=True, blank=True)
    death_date = models.DateField(verbose_name="Data decesului", null=True, blank=True)

    comorbidities = models.ManyToManyField(to=Comorbidity, verbose_name="Comorbiditati (conditii medicale existente)",
                                           blank=True)

    initial_hospital = models.ForeignKey(to=Hospital,
                                         on_delete=models.CASCADE,
                                         verbose_name="Spitalul de internare initial",
                                         related_name="initially_admitted_deaths",
                                         null=True, blank=True)
    final_hospital = models.ForeignKey(to=Hospital,
                                       on_delete=models.CASCADE,
                                       verbose_name="Spitalul decesului",
                                       related_name="finally_admitted_deaths",
                                       null=True, blank=True)

    source = models.ForeignKey(to=DataSource, on_delete=models.CASCADE, verbose_name="Sursa de date")
    parsed_text = models.TextField(verbose_name="Textul interpretat")

    validated = models.BooleanField(verbose_name="Deces validat manual", default=False)

    def __str__(self):
        collision = ''
        if self.collision_index > 1:
            collision = f' ({self.collision_index})'
        return f'{self.case_number}{collision}'


class Statistic(models.Model):
    class Meta:
        unique_together = ['field', 'groups', 'filters', 'group_by_gender', 'group_by_county']
        verbose_name = "Statistică"
        verbose_name_plural = "Statistici"

    search_string = models.CharField(null=False, blank=False, verbose_name="String de cautare", unique=True, max_length=50)

    content = models.TextField(null=False, blank=False, verbose_name="Continut")

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Data generarii statisticii")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Momentul ultimei modificari")

    field = models.CharField(max_length=25, null=True, blank=True)
    groups = models.CharField(max_length=50, null=True, blank=True)
    filters = models.CharField(max_length=255, null=True, blank=True)
    group_by_gender = models.BooleanField(default=False)
    group_by_county = models.BooleanField(default=False)

    def __str__(self):
        return f"Statistic on '{self.field}'"
