from django.template.defaultfilters import slugify as django_slugify

def slugify(name, model):    
    tempslug = django_slugify(name)
    i = 1
    if not tempslug:
        tempslug = 'blank'
    while True:
        similar = model.objects.filter(slug__startswith=tempslug)
        if not similar:
            return tempslug
        num = 2
        for sim in similar:
            try:
                new_num = int(sim.slug.split(tempslug+'_')[1])
                num = max(num, new_num)
            except ValueError: pass
            except IndexError: pass
        return tempslug + '_' + str(num+1)

