from django.db import models

# Create your models here.
# CREATE TABLE IF NOT EXISTS public.static_panel
# (
#     id integer NOT NULL DEFAULT nextval('static_panel_id_seq'::regclass),
#     date date,
#     mime time without time zone,
#     measurement numeric,
#     intensity numeric,
#     CONSTRAINT static_panel_pkey PRIMARY KEY (id)
# )

# TABLESPACE pg_default;

# ALTER TABLE IF EXISTS public.static_panel
#     OWNER to postgres;


class static_panel(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    measurement = models.IntegerField(null=False, default= 0)
    intensity = models.IntegerField(null=False, default= 0)