from django.contrib import admin
from django.utils.safestring import mark_safe

from api_core.models import Case, DataSource, Hospital, Comorbidity, Statistic


class AgeFilter(admin.SimpleListFilter):
    title = 'Vârstă'

    parameter_name = 'Vârstă'

    def lookups(self, request, model_admin):
        return (
            ('020', '0 - 20'),
            ('2040', '20 - 40'),
            ('4060', '40 - 60'),
            ('6080', '60 - 80'),
            ('80100', '80 - 100'),
        )

    def queryset(self, request, queryset):
        if self.value() == '020':
            return queryset.filter(age__gte=0,
                                   age__lte=20)
        if self.value() == '2040':
            return queryset.filter(age__gte=20,
                                   age__lte=40)
        if self.value() == '4060':
            return queryset.filter(age__gte=40,
                                   age__lte=60)
        if self.value() == '6080':
            return queryset.filter(age__gte=60,
                                   age__lte=80)
        if self.value() == '80100':
            return queryset.filter(age__gte=80,
                                   age__lte=100)


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    autocomplete_fields = ["comorbidities", "initial_hospital", "final_hospital", ]
    list_filter = ("validated", "gender", AgeFilter, "county")
    readonly_fields = ['source', 'parsed_text']
    ordering = ('-case_number', 'collision_index')
    list_display = ('case_number', 'collision_index', 'gender', 'age', 'county',
                    'test_date', 'positive_result_date', 'hospital_admission_date',
                    'death_date', 'initial_hospital',
                    'final_hospital', 'validated', 'source')
    fieldsets = (
        ('Date deduse', {
            'fields': ('case_number', 'collision_index', 'gender', 'age', 'county',
                       'test_date', 'positive_result_date', 'hospital_admission_date', 'death_date',
                       'comorbidities', 'initial_hospital', 'final_hospital',
                       'validated')
        }),
        ('Sursa de date', {
            'fields': ('source', 'parsed_text'),
        }),
    )


class CaseInline(admin.TabularInline):
    model = Case
    autocomplete_fields = ["comorbidities", "initial_hospital", "final_hospital", ]
    readonly_fields = ["parsed_text"]
    can_delete = False
    extra = 0


@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'url', 'date_created', 'status')
    save_on_top = True
    inlines = (CaseInline,)
    readonly_fields = ('date_created', 'date_modified', 'id')

    def status(self, obj):
        is_validated = True
        for case in obj.case_set.all():
            if not case.validated:
                is_validated = False
        if is_validated:
            return mark_safe("<p style='color:green'>Validated</p>")
        else:
            return mark_safe("<p style='color:red'>Not validated</p>")


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    search_fields = ['name', ]


@admin.register(Comorbidity)
class ComorbidityAdmin(admin.ModelAdmin):
    search_fields = ['name', ]


@admin.register(Statistic)
class StatisticsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'search_string', 'field', 'filters', 'groups', 'group_by_gender', 'group_by_county', 'date_created',
        'date_modified',
    )
