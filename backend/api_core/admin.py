from django.contrib import admin

from api_core.models import Case, DataSource, Hospital, Comorbidity


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    readonly_fields = ['source', 'parsed_text']
    ordering = ('-case_number', 'collision_index')
    list_display = ('case_number', 'collision_index', 'gender', 'age',
                    'test_date', 'positive_result_date', 'hospital_admission_date',
                    'death_date', 'initial_hospital',
                    'final_hospital', 'validated', 'source')
    fieldsets = (
        ('Date deduse', {
            'fields': ('case_number', 'collision_index', 'gender', 'age',
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
    list_display = ('title', 'url')
    save_on_top = True
    inlines = (CaseInline,)


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    pass


@admin.register(Comorbidity)
class ComorbidityAdmin(admin.ModelAdmin):
    pass
