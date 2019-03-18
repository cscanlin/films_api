def all_table_fields(model):
    fields_w_relationships = [field.name for field in model._meta.get_fields()]
    all_table_fields = [field.name for field in model._meta.fields]
    all_table_fields += [rel_field for rel_field in fields_w_relationships
                         if rel_field not in all_table_fields]

    if hasattr(model, 'calculated_properties'):
        all_table_fields += list(model.calculated_properties().keys())

    return all_table_fields
