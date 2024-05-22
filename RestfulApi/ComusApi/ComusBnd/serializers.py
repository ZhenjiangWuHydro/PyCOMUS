from rest_framework import serializers

from .models import ComusSHBModel, ComusGHBModel, ComusRCHModel, ComusWELModel, ComusDRNModel, ComusEVTModel, \
    ComusHFBModel, ComusRIVModel, ComusIBSModel, ComusSTRCtrlModel, ComusSTRPeriodModel, ComusSTRGridModel, \
    ComusSTRWaterUseModel, ComusSTRDrnModel, ComusRESCtrlModel, ComusRESPeriodModel, ComusRESGridModel, \
    ComusLAKCtrlModel, ComusLAKPeriodModel, ComusLAKGridModel, ComusREGModel, ComusSUBCtrlModel, ComusSUBMzModel, \
    ComusSUBNdbLyrModel, ComusSUBNdbGridModel, ComusSUBDbLyrModel, ComusSUBDbGridModel


class ComusSHBSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComusSHBModel
        exclude = ['comus_dis']
        read_only_fields = ['comus_dis']

    def validate(self, data):
        if "data" not in data:
            raise serializers.ValidationError("The input parameter must include the 'data' parameter.")
        return data


class ComusGHBSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComusGHBModel
        exclude = ['comus_dis']
        read_only_fields = ['comus_dis']

    def validate(self, data):
        if "data" not in data:
            raise serializers.ValidationError("The input parameter must include the 'data' parameter.")
        return data


class ComusRCHSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComusRCHModel
        exclude = ['comus_dis']
        read_only_fields = ['comus_dis']

    def validate(self, data):
        if "data" not in data:
            raise serializers.ValidationError("The input parameter must include the 'data' parameter.")
        return data


class ComusWELSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComusWELModel
        exclude = ['comus_dis']
        read_only_fields = ['comus_dis']

    def validate(self, data):
        if "data" not in data:
            raise serializers.ValidationError("The input parameter must include the 'data' parameter.")
        return data


class ComusDRNSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComusDRNModel
        exclude = ['comus_dis']
        read_only_fields = ['comus_dis']

    def validate(self, data):
        if "data" not in data:
            raise serializers.ValidationError("The input parameter must include the 'data' parameter.")
        return data


class ComusEVTSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComusEVTModel
        exclude = ['comus_dis']
        read_only_fields = ['comus_dis']

    def validate(self, data):
        if "data" not in data:
            raise serializers.ValidationError("The input parameter must include the 'data' parameter.")
        if "evt" not in data:
            raise serializers.ValidationError("The input parameter must include the 'evt' parameter.")
        if "num_seg" not in data:
            raise serializers.ValidationError("The input parameter must include the 'num_seg' parameter.")
        evt = int(data["evt"])
        num_seg = int(data["num_seg"])
        if evt not in (1, 2):
            raise serializers.ValidationError("'evt' should be 1 or 2.")
        if num_seg < 2 or num_seg > 20:
            raise serializers.ValidationError(
                "'num_seg' should be less than or equal to 20 and greater than or equal to 2.")
        return data


class ComusHFBSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComusHFBModel
        exclude = ['comus_dis']
        read_only_fields = ['comus_dis']

    def validate(self, data):
        if "data" not in data:
            raise serializers.ValidationError("The input parameter must include the 'data' parameter.")
        return data


class ComusRIVSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComusRIVModel
        exclude = ['comus_dis']
        read_only_fields = ['comus_dis']

    def validate(self, data):
        if "data" not in data:
            raise serializers.ValidationError("The input parameter must include the 'data' parameter.")
        return data


class ComusIBSSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComusIBSModel
        exclude = ['comus_dis']
        read_only_fields = ['comus_dis']

    def validate(self, data):
        if "data" not in data:
            raise serializers.ValidationError(f"The 'data' field is required.")
        return data


class ComusSTRCtrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComusSTRCtrlModel
        exclude = ['comus_dis']
        read_only_fields = ['comus_dis']

    def validate(self, data):
        if "data" not in data:
            raise serializers.ValidationError("The input parameter must include the 'data' parameter.")
        if not isinstance(data, dict):
            raise serializers.ValidationError("The 'data' field must be a dictionary.")
        keys = sorted(data["data"].keys(), key=lambda x: int(x))
        expected_keys = [str(i) for i in range(1, len(keys) + 1)]
        if keys != expected_keys:
            raise serializers.ValidationError("The keys in the 'data' dictionary must start from 1 and be consecutive.")
        for key, value in data["data"].items():
            if not isinstance(int(key), int):
                raise serializers.ValidationError("Each key in the 'data' dictionary must be an integer.")
            if not isinstance(value, list) or len(value) != 9:
                raise serializers.ValidationError(
                    "Each value in the 'data' dictionary must be a list of exactly 9 integers.")
            if not all(isinstance(item, int) for item in value):
                raise serializers.ValidationError("Each item in the lists of the 'data' dictionary must be an integer.")
        return data


class ComusSTRPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComusSTRPeriodModel
        exclude = ['comus_dis']
        read_only_fields = ['comus_dis']

    def validate(self, data):
        if "data" not in data:
            raise serializers.ValidationError("The input parameter must include the 'data' parameter.")
        return data


class ComusSTRGridSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComusSTRGridModel
        exclude = ['comus_dis']
        read_only_fields = ['comus_dis']

    def validate(self, data):
        if "data" not in data:
            raise serializers.ValidationError("The input parameter must include the 'data' parameter.")
        return data


class ComusSTRWaterUseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComusSTRWaterUseModel
        exclude = ['comus_dis']
        read_only_fields = ['comus_dis']
    def validate(self, data):
        if "data" not in data:
            raise serializers.ValidationError("The input parameter must include the 'data' parameter.")
        return data


class ComusSTRDrnSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComusSTRDrnModel
        exclude = ['comus_dis']
        read_only_fields = ['comus_dis']
    def validate(self, data):
        if "data" not in data:
            raise serializers.ValidationError("The input parameter must include the 'data' parameter.")
        return data


class ComusRESCtrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComusRESCtrlModel
        exclude = ['comus_dis']
        read_only_fields = ['comus_dis']

    def validate(self, data):
        if "data" not in data:
            raise serializers.ValidationError("The input parameter must include the 'data' parameter.")
        if not isinstance(data, dict):
            raise serializers.ValidationError("The 'data' field must be a dictionary.")
        for key, value in data["data"].items():
            if not isinstance(int(key), int):
                raise serializers.ValidationError("Each key in the 'data' dictionary must be an integer.")
            if not isinstance(value, list) or len(value) != 4:
                raise serializers.ValidationError(
                    "Each value in the 'data' dictionary must be a list of exactly 4 integers.")
            if not all(isinstance(item, (int, float)) for item in value):
                raise serializers.ValidationError(
                    "Each item in the lists of the 'data' dictionary must be an integer/float.")
        return data


class ComusRESPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComusRESPeriodModel
        exclude = ['comus_dis']
        read_only_fields = ['comus_dis']

    def validate(self, data):
        if "data" not in data:
            raise serializers.ValidationError("The input parameter must include the 'data' parameter.")
        return data


class ComusRESGridSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComusRESGridModel
        exclude = ['comus_dis']
        read_only_fields = ['comus_dis']

    def validate(self, data):
        if "data" not in data:
            raise serializers.ValidationError("The input parameter must include the 'data' parameter.")
        return data


class ComusLAKCtrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComusLAKCtrlModel
        exclude = ['comus_dis']
        read_only_fields = ['comus_dis']

    def validate(self, data):
        if "data" not in data:
            raise serializers.ValidationError("The input parameter must include the 'data' parameter.")
        if not isinstance(data, dict):
            raise serializers.ValidationError("The 'data' field must be a dictionary.")
        for key, value in data["data"].items():
            if not isinstance(int(key), int):
                raise serializers.ValidationError("Each key in the 'data' dictionary must be an integer.")
            if not isinstance(value, list) or len(value) != 13:
                raise serializers.ValidationError(
                    "Each value in the 'data' dictionary must be a list of exactly 13 integers/floats.")
            if not all(isinstance(item, (int, float)) for item in value):
                raise serializers.ValidationError(
                    "Each item in the lists of the 'data' dictionary must be an integer/float.")
        return data


class ComusLAKPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComusLAKPeriodModel
        exclude = ['comus_dis']
        read_only_fields = ['comus_dis']

    def validate(self, data):
        if "data" not in data:
            raise serializers.ValidationError("The input parameter must include the 'data' parameter.")
        return data


class ComusLAKGridSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComusLAKGridModel
        exclude = ['comus_dis']
        read_only_fields = ['comus_dis']

    def validate(self, data):
        if "data" not in data:
            raise serializers.ValidationError("The input parameter must include the 'data' parameter.")
        return data


class ComusREGSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComusREGModel
        exclude = ['comus_dis']
        read_only_fields = ['comus_dis']

    def validate(self, data):
        if "data" not in data:
            raise serializers.ValidationError("The input parameter must include the 'data' parameter.")
        return data


class ComusSUBCtrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComusSUBCtrlModel
        exclude = ['comus_dis']
        read_only_fields = ['comus_dis']

    def validate(self, data):
        if "num_ndb" not in data:
            raise serializers.ValidationError("The input parameter must include the 'num_ndb' parameter.")
        if "num_db" not in data:
            raise serializers.ValidationError("The input parameter must include the 'num_db' parameter.")
        if "num_mz" not in data:
            raise serializers.ValidationError("The input parameter must include the 'num_mz' parameter.")
        if "nn" not in data:
            raise serializers.ValidationError("The input parameter must include the 'nn' parameter.")
        if "acc" not in data:
            raise serializers.ValidationError("The input parameter must include the 'acc' parameter.")
        if "it_min" not in data:
            raise serializers.ValidationError("The input parameter must include the 'it_min' parameter.")
        if "dsh_opt" not in data:
            raise serializers.ValidationError("The input parameter must include the 'dsh_opt' parameter.")

        num_ndb = data.get('num_ndb')
        num_db = data.get('num_db')
        num_mz = data.get('num_mz')
        nn = data.get('nn')
        acc = data.get('acc')
        dsh_opt = data.get('dsh_opt')

        if num_ndb < 0 or num_db < 0:
            raise serializers.ValidationError(
                "The parameters 'num_ndb' and 'num_db' must be greater than or equal to 0. Please check!")
        if num_ndb + num_db == 0:
            raise serializers.ValidationError(
                "The parameters 'num_ndb' and 'num_db' must have at least one value not equal to 0. Please check!")
        if num_db > 0:
            if num_mz <= 0:
                raise serializers.ValidationError(
                    "When simulating delayed confining units, the 'num_mz' parameter cannot be set to 0. Please check!")
            if nn <= 5 or nn >= 100:
                raise serializers.ValidationError("The valid range for the 'nn' parameter is 5 to 100. Please check!")
            if acc < 0 or acc > 0.6:
                raise serializers.ValidationError(
                    "The valid range for the 'acc' parameter is 0.0 to 0.6. Please check!")
            if dsh_opt not in (1, 2):
                raise serializers.ValidationError("The 'dsh_opt' parameter must be either 1 or 2. Please check!")
        return data


class ComusSUBMzSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComusSUBMzModel
        exclude = ['comus_dis']
        read_only_fields = ['comus_dis']

    def validate(self, data):
        if "data" not in data:
            raise serializers.ValidationError("The input parameter must include the 'data' parameter.")
        return data


class ComusSUBNdbLyrSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComusSUBNdbLyrModel
        exclude = ['comus_dis']
        read_only_fields = ['comus_dis']

    def validate(self, data):
        if "data" not in data:
            raise serializers.ValidationError("The input parameter must include the 'data' parameter.")
        return data


class ComusSUBNdbGridSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComusSUBNdbGridModel
        exclude = ['comus_dis']
        read_only_fields = ['comus_dis']

    def validate(self, data):
        if "data" not in data:
            raise serializers.ValidationError("The input parameter must include the 'data' parameter.")
        return data


class ComusSUBDbLyrSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComusSUBDbLyrModel
        exclude = ['comus_dis']
        read_only_fields = ['comus_dis']

    def validate(self, data):
        if "data" not in data:
            raise serializers.ValidationError("The input parameter must include the 'data' parameter.")
        return data


class ComusSUBDbGridSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComusSUBDbGridModel
        exclude = ['comus_dis']
        read_only_fields = ['comus_dis']

    def validate(self, data):
        if "data" not in data:
            raise serializers.ValidationError("The input parameter must include the 'data' parameter.")
        return data
