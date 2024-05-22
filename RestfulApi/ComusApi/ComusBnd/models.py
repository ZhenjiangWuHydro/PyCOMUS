from django.db import models


class ComusSHBModel(models.Model):
    comus_dis = models.OneToOneField('ComusDis.ComusDisModel', on_delete=models.CASCADE, primary_key=True)
    data = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'comus_shb'


class ComusGHBModel(models.Model):
    comus_dis = models.OneToOneField('ComusDis.ComusDisModel', on_delete=models.CASCADE, primary_key=True)
    data = models.JSONField(null=True, blank=True)
    class Meta:
        db_table = 'comus_ghb'


class ComusRCHModel(models.Model):
    comus_dis = models.OneToOneField('ComusDis.ComusDisModel', on_delete=models.CASCADE, primary_key=True)
    data = models.JSONField(null=True, blank=True)
    rech = models.IntegerField(default=1)

    class Meta:
        db_table = 'comus_rch'


class ComusWELModel(models.Model):
    comus_dis = models.OneToOneField('ComusDis.ComusDisModel', on_delete=models.CASCADE, primary_key=True)
    data = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'comus_wel'


class ComusDRNModel(models.Model):
    comus_dis = models.OneToOneField('ComusDis.ComusDisModel', on_delete=models.CASCADE, primary_key=True)
    data = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'comus_drn'


class ComusEVTModel(models.Model):
    comus_dis = models.OneToOneField('ComusDis.ComusDisModel', on_delete=models.CASCADE, primary_key=True)
    data = models.JSONField(null=True, blank=True)
    evt = models.IntegerField(default=1)
    num_seg = models.IntegerField(default=10)

    class Meta:
        db_table = 'comus_evt'


class ComusHFBModel(models.Model):
    comus_dis = models.OneToOneField('ComusDis.ComusDisModel', on_delete=models.CASCADE, primary_key=True)
    data = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'comus_hfb'


class ComusRIVModel(models.Model):
    comus_dis = models.OneToOneField('ComusDis.ComusDisModel', on_delete=models.CASCADE, primary_key=True)
    data = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'comus_riv'


class ComusIBSModel(models.Model):
    comus_dis = models.OneToOneField('ComusDis.ComusDisModel', on_delete=models.CASCADE, primary_key=True)
    data = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'comus_ibs'


class ComusSTRCtrlModel(models.Model):
    comus_dis = models.OneToOneField('ComusDis.ComusDisModel', on_delete=models.CASCADE, primary_key=True)
    data = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'comus_str_ctrl'


class ComusSTRPeriodModel(models.Model):
    comus_dis = models.OneToOneField('ComusDis.ComusDisModel', on_delete=models.CASCADE, primary_key=True)
    data = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'comus_str_period'


class ComusSTRGridModel(models.Model):
    comus_dis = models.OneToOneField('ComusDis.ComusDisModel', on_delete=models.CASCADE, primary_key=True)
    data = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'comus_str_grid'


class ComusSTRWaterUseModel(models.Model):
    comus_dis = models.OneToOneField('ComusDis.ComusDisModel', on_delete=models.CASCADE, primary_key=True)
    data = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'comus_str_water_use'


class ComusSTRDrnModel(models.Model):
    comus_dis = models.OneToOneField('ComusDis.ComusDisModel', on_delete=models.CASCADE, primary_key=True)
    data = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'comus_str_drn'


class ComusRESCtrlModel(models.Model):
    comus_dis = models.OneToOneField('ComusDis.ComusDisModel', on_delete=models.CASCADE, primary_key=True)
    data = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'comus_res_ctrl'


class ComusRESPeriodModel(models.Model):
    comus_dis = models.OneToOneField('ComusDis.ComusDisModel', on_delete=models.CASCADE, primary_key=True)
    data = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'comus_res_period'


class ComusRESGridModel(models.Model):
    comus_dis = models.OneToOneField('ComusDis.ComusDisModel', on_delete=models.CASCADE, primary_key=True)
    data = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'comus_res_grid'


class ComusLAKCtrlModel(models.Model):
    comus_dis = models.OneToOneField('ComusDis.ComusDisModel', on_delete=models.CASCADE, primary_key=True)
    data = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'comus_lak_ctrl'


class ComusLAKPeriodModel(models.Model):
    comus_dis = models.OneToOneField('ComusDis.ComusDisModel', on_delete=models.CASCADE, primary_key=True)
    data = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'comus_lak_period'


class ComusLAKGridModel(models.Model):
    comus_dis = models.OneToOneField('ComusDis.ComusDisModel', on_delete=models.CASCADE, primary_key=True)
    data = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'comus_lak_grid'


class ComusREGModel(models.Model):
    comus_dis = models.OneToOneField('ComusDis.ComusDisModel', on_delete=models.CASCADE, primary_key=True)
    data = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'comus_reg'


class ComusSUBCtrlModel(models.Model):
    comus_dis = models.OneToOneField('ComusDis.ComusDisModel', on_delete=models.CASCADE, primary_key=True)
    num_ndb = models.IntegerField()
    num_db = models.IntegerField()
    num_mz = models.IntegerField()
    nn = models.IntegerField()
    acc = models.FloatField()
    it_min = models.IntegerField()
    dsh_opt = models.IntegerField()

    class Meta:
        db_table = 'comus_sub_ctrl'


class ComusSUBMzModel(models.Model):
    comus_dis = models.OneToOneField('ComusDis.ComusDisModel', on_delete=models.CASCADE, primary_key=True)
    data = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'comus_sub_mz'


class ComusSUBNdbLyrModel(models.Model):
    comus_dis = models.OneToOneField('ComusDis.ComusDisModel', on_delete=models.CASCADE, primary_key=True)
    data = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'comus_sub_ndb_lyr'


class ComusSUBNdbGridModel(models.Model):
    comus_dis = models.OneToOneField('ComusDis.ComusDisModel', on_delete=models.CASCADE, primary_key=True)
    data = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'comus_sub_ndb_grid'


class ComusSUBDbLyrModel(models.Model):
    comus_dis = models.OneToOneField('ComusDis.ComusDisModel', on_delete=models.CASCADE, primary_key=True)
    data = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'comus_sub_db_lyr'


class ComusSUBDbGridModel(models.Model):
    comus_dis = models.OneToOneField('ComusDis.ComusDisModel', on_delete=models.CASCADE, primary_key=True)
    data = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'comus_sub_db_grid'
