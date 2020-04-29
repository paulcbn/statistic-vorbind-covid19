from django.contrib import admin

from api_core.models import Case, DataSource, Hospital, Comorbidity


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
    list_filter = ("validated", "gender", AgeFilter)
    readonly_fields = ['source', 'parsed_text']
    ordering = ('-case_number', 'collision_index')
    list_display = ('case_number', 'collision_index', 'gender', 'age',
                    'test_date', 'positive_result_date', 'hospital_admission_date',
                    'death_date', 'initial_hospital',
                    'final_hospital', 'validated', 'source')
    search_fields = ['age', ]
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
    list_display = ('id', 'title', 'url', 'date_created')
    save_on_top = True
    inlines = (CaseInline,)
    readonly_fields = ('date_created', 'date_modified', 'id')


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    pass


@admin.register(Comorbidity)
class ComorbidityAdmin(admin.ModelAdmin):
    pass
