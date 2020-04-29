from django.contrib import admin
from django.utils.safestring import mark_safe

from api_core.models import Case, DataSource, Hospital, Comorbidity, Statistic


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
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
    pass


@admin.register(Comorbidity)
class ComorbidityAdmin(admin.ModelAdmin):
    pass


@admin.register(Statistic)
class StatisticsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'search_string', 'field', 'filters', 'groups', 'group_by_gender', 'group_by_county', 'date_created',
        'date_modified',
    )
