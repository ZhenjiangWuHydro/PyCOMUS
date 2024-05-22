from rest_framework import serializers

from .models import ComusDisModel, ComusCtrlParsModel, ComusOutParsModel, ComusSpaceModel, ComusLpfPropModel, \
    ComusBcfPropModel, ComusGridParsModel, ComusPeriodModel


class ComusModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComusDisModel
        fields = ['user_name', 'project_name']


class ComusCtrlParsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComusCtrlParsModel
        exclude = ['comus_dis']
        read_only_fields = ['comus_dis']

    def validate(self, data):
        sim_mtd = data.get('sim_mtd', 1)
        sim_type = data.get('sim_type', 2)
        acc_lambda = data.get('acc_lambda', -1)
        intblkm = data.get('intblkm', 1)
        solve = data.get('solve', 2)
        max_iter = data.get('max_iter', 200)
        damp = data.get('damp', 1)
        h_close = data.get('h_close', 0.0001)
        r_close = data.get('r_close', 0.001)
        relax = data.get('relax', 0)
        theta = data.get('theta', 0.7)
        gamma = data.get('gamma', 3)
        akappa = data.get('akappa', 0.001)
        n_iter = data.get('n_iter', 5)
        ch_flg = data.get('ch_flg', 0)
        wd_flg = data.get('wd_flg', 0)
        wet_fct = data.get('wet_fct', 0.1)
        newt_iter = data.get('newt_iter', 1)
        hd_wet = data.get('hd_wet', 1)
        reg_sta = data.get('reg_sta', 0)
        mul_td = data.get('mul_td', 0)
        num_td = data.get('num_td', -1)

        if sim_mtd not in [1, 2]:
            raise serializers.ValidationError("The 'sim_mtd' parameter must be 1 or 2. Please check!")

        if sim_type not in [1, 2]:
            raise serializers.ValidationError("The 'sim_type' parameter must be 1 or 2. Please check!")

        if sim_mtd == 1 and sim_type == 1:
            if not (1E-4 <= acc_lambda <= 1E-3) and abs(acc_lambda + 1.0) > 1e-10:
                raise serializers.ValidationError(
                    "The valid range for the 'acc_lambda' parameter is from 0.0001 to 0.001 or it can be -1.0. Please check!")

        if intblkm not in [1, 2]:
            raise serializers.ValidationError("The 'intblkm' parameter must be 1 or 2. Please check!")

        if solve not in [1, 2]:
            raise serializers.ValidationError("The 'solve' parameter must be 1 or 2. Please check!")

        if not (200 <= max_iter <= 1000000):
            raise serializers.ValidationError(
                "The valid range for the 'max_iter' parameter is from 200 to 1000000. Please check!")

        if not (0.0001 <= damp <= 1.0):
            raise serializers.ValidationError(
                "The valid range for the 'damp' parameter is from 0.0001 to 1.0. Please check!")

        if not (1e-8 <= h_close <= 1e-1):
            raise serializers.ValidationError(
                "The valid range for the 'h_close' parameter is from 0.1 to 1e-8. Please check!")

        if solve == 2 and not (1e-8 <= r_close <= 1e-1):
            raise serializers.ValidationError(
                "The valid range for the 'r_close' parameter is from 0.1 to 1e-8. Please check!")

        if relax not in [0, 1]:
            raise serializers.ValidationError("The 'relax' parameter value must be 0 or 1. Please check!")

        if relax == 1:
            if not (0.35 <= theta <= 0.95):
                raise serializers.ValidationError(
                    "The valid range for the 'theta' parameter is from 0.35 to 0.95. Please check!")
            if not (1.0 <= gamma <= 5.0):
                raise serializers.ValidationError(
                    "The valid range for the 'gamma' parameter is from 1.0 to 5.0. Please check!")
            if not (0.0 < akappa <= 0.2):
                raise serializers.ValidationError(
                    "The valid range for the 'akappa' parameter is from 0.0 (exclusive) to 0.2. Please check!")
            if not (0 <= n_iter <= 100):
                raise serializers.ValidationError(
                    "The valid range for the 'n_iter' parameter is from 0 to 100. Please check!")

        if ch_flg not in [0, 1]:
            raise serializers.ValidationError("The 'ch_flg' parameter must be 0 or 1. Please check!")

        if sim_mtd == 2:
            if wd_flg not in [0, 1]:
                raise serializers.ValidationError("The 'wd_flg' parameter must be 0 or 1. Please check!")

            if wd_flg == 1:
                if not (-1.0 <= wet_fct <= 1.0 and wet_fct > 0.0):
                    raise serializers.ValidationError(
                        "The 'wet_fct' parameter should be entered as -1 or a valid value between 0.0 and 1.0 (Note: it should be greater than 0.0 and can be equal to 1.0). Please check!")

                if not (1 <= newt_iter <= 4):
                    raise serializers.ValidationError(
                        "The valid range for the 'newt_iter' parameter is from 1 to 4. Please check!")

                if hd_wet not in [-1, 1, 2]:
                    raise serializers.ValidationError("The 'hd_wet' parameter must be -1, 1, or 2. Please check!")

        if reg_sta not in [0, 1]:
            raise serializers.ValidationError("The 'reg_sta' parameter must be 0 or 1. Please check!")

        if mul_td not in [0, 1]:
            raise serializers.ValidationError("The 'mul_td' parameter must be 0 or 1. Please check!")

        if mul_td == 1:
            if not (-1 <= num_td <= 256 and num_td not in [-1, 0, 1]):
                raise serializers.ValidationError(
                    "The 'num_td' parameter must be either -1 or within the range of 2 to 256. Please check!")

        return data


class ComusOutParsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComusOutParsModel
        exclude = ['comus_dis']
        read_only_fields = ['comus_dis']

    def validate(self, data):
        for field_name, field_value in data.items():
            if field_value not in [0, 1, 2]:
                raise serializers.ValidationError(f"The '{field_name}' parameter must be 0, 1, or 2. Please check!")
        return data


class ComusSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComusSpaceModel
        exclude = ['comus_dis']
        read_only_fields = ['comus_dis']

    def validate(self, data):
        atti_data = data.get('data', {})
        atti = atti_data.get('atti', [])
        num_id = atti_data.get('num_id', [])
        delt = atti_data.get('delt', [])
        if not atti or not num_id or not delt:
            raise serializers.ValidationError("atti, num_id, and delt are required fields")
        if not all(char in ['R', 'C'] for char in atti):
            raise serializers.ValidationError("atti should contain only 'R' or 'C'")
        if not all(num >= 1 for num in num_id):
            raise serializers.ValidationError("num_id should be greater than or equal to 1")
        if not all(d > 0 for d in delt):
            raise serializers.ValidationError("delt should be greater than 0")
        if len(atti) != len(num_id) or len(atti) != len(delt):
            raise serializers.ValidationError("atti, num_id, and delt should have the same number of elements")

        return data


class ComusLpfPropSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComusLpfPropModel
        exclude = ['comus_dis']
        read_only_fields = ['comus_dis']

    def validate(self, data):
        type_list = data.get('data', {}).get('type', [])
        cbd_list = data.get('data', {}).get('cbd', [])
        ibs_list = data.get('data', {}).get('ibs', [])
        if not type_list or not cbd_list or not ibs_list:
            raise serializers.ValidationError("type, cbd, and ibs are required fields")
        if not all(type in [0, 1] for type in type_list):
            raise serializers.ValidationError("type should contain only '0' or '1'")
        if not all(cbd in [0, 1] for cbd in cbd_list):
            raise serializers.ValidationError("cbd should contain only '0' or '1'")
        if not all(ibs in [0, 1] for ibs in ibs_list):
            raise serializers.ValidationError("ibs should contain only '0' or '1'")
        if len(type_list) != len(cbd_list) or len(type_list) != len(ibs_list):
            raise serializers.ValidationError("type, cbd, and ibs should have the same number of elements")
        return data


class ComusBcfPropSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComusBcfPropModel
        exclude = ['comus_dis']
        read_only_fields = ['comus_dis']

    def validate(self, data):
        type_list = data.get('data', {}).get('type', [])
        trpy_list = data.get('data', {}).get('trpy', [])
        ibs_list = data.get('data', {}).get('ibs', [])
        if not type_list or not trpy_list or not ibs_list:
            raise serializers.ValidationError("type, trpy, and ibs are required fields")

        if not all(type in [0, 1, 2, 3] for type in type_list):
            raise serializers.ValidationError("type should contain only '0', '1', '2', or '3'")
        if not all(ibs in [0, 1] for ibs in ibs_list):
            raise serializers.ValidationError("ibs should contain only '0' or '1'")
        if len(type_list) != len(trpy_list) or len(type_list) != len(ibs_list):
            raise serializers.ValidationError("type, trpy, and ibs should have the same number of elements")
        if not all(isinstance(trpy, (int, float)) and trpy > 0 for trpy in trpy_list):
            raise serializers.ValidationError("trpy should contain only positive numbers")
        return data


class ComusGridParsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComusGridParsModel
        exclude = ['comus_dis']
        read_only_fields = ['comus_dis']

    def validate(self, data):
        par_name_list = ["top", "bot", "ibound", "shead", "kx", "transm", "vcont", "sc1", "sc2", "wet_dry", "ky", "kz",
                         "vkcb", "tkcb"]
        if 'data' in data:
            for key in data['data'].keys():
                if key not in par_name_list:
                    raise serializers.ValidationError(
                        f"'{key}' should be one of {par_name_list}.")
        else:
            serializers.ValidationError("The term 'data' needs to be passed as a parameter.")
        return data

    def create(self, validated_data):
        data = validated_data.pop('data', {})
        comus_dis = validated_data.pop('comus_dis')
        instance = ComusGridParsModel.objects.create(comus_dis=comus_dis, data=data)
        return instance

    def update(self, instance, validated_data):
        data = validated_data.pop('data', {})
        for key, value in data.items():
            instance.data[key] = value
        instance.save()
        return instance


class ComusPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComusPeriodModel
        exclude = ['comus_dis']
        read_only_fields = ['comus_dis']

    def validate(self, data):
        period_data = data.get("period", {})
        if not isinstance(period_data, dict):
            raise serializers.ValidationError("'period' must be a dictionary.")

        if not all(key.isdigit() for key in period_data.keys()):
            raise serializers.ValidationError("Keys in 'period' must be numeric.")

        expected_keys = list(range(1, len(period_data) + 1))
        actual_keys = sorted(map(int, period_data.keys()))
        if actual_keys != expected_keys:
            raise serializers.ValidationError("Keys in 'period' must start from 1 and be continuous.")

        for key, value in period_data.items():
            if not isinstance(value, dict):
                raise serializers.ValidationError(f"Value for key {key} must be a dictionary.")
            if 'period_len' not in value or 'num_step' not in value or 'multr' not in value:
                raise serializers.ValidationError(
                    f"Value for key {key} must contain 'period_len', 'num_step', and 'multr'.")
            if not isinstance(value['period_len'], int) or not isinstance(value['num_step'], int):
                raise serializers.ValidationError(f"'period_len' and 'num_step' for key {key} must be integers.")
            if not isinstance(value['multr'], (int, float)):
                raise serializers.ValidationError(f"'multr' for key {key} must be a number.")
            if value['period_len'] <= 0 or value['num_step'] <= 0 or value['multr'] <= 0:
                raise serializers.ValidationError(
                    f"'period_len', 'num_step', and 'multr' for key {key} must be greater than 0.")

        return data


