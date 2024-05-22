from ComusDis.models import ComusDisModel, ComusCtrlParsModel, ComusPeriodModel
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ComusSHBModel, ComusGHBModel, ComusRCHModel, ComusWELModel, ComusDRNModel, ComusEVTModel, \
    ComusHFBModel, ComusRIVModel, ComusIBSModel, ComusSTRCtrlModel, ComusSTRPeriodModel, ComusSTRGridModel, \
    ComusSTRWaterUseModel, ComusSTRDrnModel, ComusRESCtrlModel, ComusRESPeriodModel, ComusRESGridModel, \
    ComusLAKCtrlModel, ComusLAKPeriodModel, ComusLAKGridModel, ComusREGModel, ComusSUBCtrlModel, ComusSUBMzModel, \
    ComusSUBNdbLyrModel, ComusSUBNdbGridModel, ComusSUBDbLyrModel, ComusSUBDbGridModel
from .serializers import ComusSHBSerializer, ComusGHBSerializer, ComusRCHSerializer, ComusWELSerializer, \
    ComusDRNSerializer, ComusEVTSerializer, ComusHFBSerializer, ComusRIVSerializer, ComusIBSSerializer, \
    ComusSTRCtrlSerializer, ComusSTRPeriodSerializer, ComusSTRGridSerializer, ComusSTRWaterUseSerializer, \
    ComusSTRDrnSerializer, ComusRESCtrlSerializer, ComusRESPeriodSerializer, ComusRESGridSerializer, \
    ComusLAKCtrlSerializer, ComusLAKPeriodSerializer, ComusLAKGridSerializer, ComusREGSerializer, \
    ComusSUBCtrlSerializer, ComusSUBMzSerializer, ComusSUBNdbLyrSerializer, ComusSUBNdbGridSerializer, \
    ComusSUBDbLyrSerializer, ComusSUBDbGridSerializer


def validate_values(head, num_lyr, num_row, num_col, field_count, period_count):
    if not isinstance(head, dict):
        return f"'{head}' must be a dictionary"
    for key, value in head.items():
        try:
            key_int = int(key)
            if key_int < 1 or key_int > period_count:
                return f"Dict '{key}' is out of range (1-{period_count})"
        except ValueError:
            return f"Dict '{key}' is not an integer"

        if not isinstance(value, list):
            return f"Value for key '{key}' is not a list"
        for sublist in value:
            if not isinstance(sublist, list):
                return f"Sublist in value for key '{key}' is not a list"
            if len(sublist) != field_count:
                return f"Sublist in value for key '{key}' does not contain exactly '{field_count}' elements"
            layer, row, col, *_ = sublist
            if not (1 <= layer <= num_lyr):
                return f"Layer value {layer} in sublist for key '{key}' is out of range (1-{num_lyr})"
            if not (1 <= row <= num_row):
                return f"Row value {row} in sublist for key '{key}' is out of range (1-{num_row})"
            if not (1 <= col <= num_col):
                return f"Column value {col} in sublist for key '{key}' is out of range (1-{num_col})"
    return None


class ComusSHBView(APIView):
    def get(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            shb = ComusSHBModel.objects.get(comus_dis=comus_dis)
            serializer = ComusSHBSerializer(shb)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ComusDisModel.DoesNotExist, ComusSHBModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its SHB parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = ComusSHBSerializer(data=request.data)
        user_name = request.data.get('user_name')
        project_name = request.data.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            try:
                shb = ComusSHBModel.objects.get(comus_dis=comus_dis)
                serializer = ComusSHBSerializer(shb, data=request.data, partial=True)
                print(serializer)
            except ComusSHBModel.DoesNotExist:
                pass

            if serializer.is_valid():
                try:
                    period = ComusPeriodModel.objects.get(comus_dis=comus_dis)
                    period_count = len(period.period.keys())
                except ComusPeriodModel.DoesNotExist:
                    return Response({'error': 'ComusPeriodModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)
                try:
                    ctrl_pars = ComusCtrlParsModel.objects.get(comus_dis=comus_dis)
                    num_lyr = ctrl_pars.num_layer
                    num_row = ctrl_pars.num_row
                    num_col = ctrl_pars.num_col
                    data = request.data.get('data')
                    data_error = validate_values(data, num_lyr, num_row, num_col, 5, period_count)
                    if data_error:
                        return Response({"error": f"Invalid 'data' values: {data_error}"},
                                        status=status.HTTP_400_BAD_REQUEST)

                except ComusCtrlParsModel.DoesNotExist:
                    return Response({'error': 'ComusCtrlParsModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)
                serializer.save(comus_dis=comus_dis)
                if 'shb' in locals():
                    message = 'COMUS SHB parameters updated successfully'
                else:
                    message = 'COMUS SHB parameters saved successfully'
                return Response({'message': message}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ComusDisModel.DoesNotExist:
            return Response({'error': 'This COMUS model not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            shb = ComusSHBModel.objects.get(comus_dis=comus_dis)
            shb.delete()
            return Response({'success': 'COMUS SHB parameters deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)
        except (ComusDisModel.DoesNotExist, ComusSHBModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its SHB parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)


class ComusGHBView(APIView):
    def get(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            ghb = ComusGHBModel.objects.get(comus_dis=comus_dis)
            serializer = ComusGHBSerializer(ghb)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ComusDisModel.DoesNotExist, ComusGHBModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its GHB parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = ComusGHBSerializer(data=request.data)
        user_name = request.data.get('user_name')
        project_name = request.data.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            try:
                ghb = ComusGHBModel.objects.get(comus_dis=comus_dis)
                serializer = ComusGHBSerializer(ghb, data=request.data, partial=True)
            except ComusGHBModel.DoesNotExist:
                pass
            if serializer.is_valid():
                try:
                    period = ComusPeriodModel.objects.get(comus_dis=comus_dis)
                    period_count = len(period.period.keys())
                except ComusPeriodModel.DoesNotExist:
                    return Response({'error': 'ComusPeriodModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)
                try:
                    ctrl_pars = ComusCtrlParsModel.objects.get(comus_dis=comus_dis)
                    num_lyr = ctrl_pars.num_layer
                    num_row = ctrl_pars.num_row
                    num_col = ctrl_pars.num_col
                    data = request.data.get('data')
                    data_error = validate_values(data, num_lyr, num_row, num_col, 6, period_count)
                    if data_error:
                        return Response({"error": f"Invalid 'data' values: {data_error}"},
                                        status=status.HTTP_400_BAD_REQUEST)

                except ComusCtrlParsModel.DoesNotExist:
                    return Response({'error': 'ComusCtrlParsModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)
                serializer.save(comus_dis=comus_dis)
                if 'ghb' in locals():
                    message = 'COMUS GHB parameters updated successfully'
                else:
                    message = 'COMUS GHB parameters saved successfully'
                return Response({'message': message}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (ComusDisModel.DoesNotExist):
            return Response({'error': 'This COMUS model not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')

        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            ghb = ComusGHBModel.objects.get(comus_dis=comus_dis)
            ghb.delete()
            return Response({'success': 'COMUS GHB parameters deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)
        except (ComusDisModel.DoesNotExist, ComusGHBModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its GHB parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)


class ComusRCHView(APIView):
    def get(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            rch = ComusRCHModel.objects.get(comus_dis=comus_dis)
            serializer = ComusRCHSerializer(rch)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ComusDisModel.DoesNotExist, ComusRCHModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its RCH parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = ComusRCHSerializer(data=request.data)
        user_name = request.data.get('user_name')
        project_name = request.data.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            try:
                rch = ComusRCHModel.objects.get(comus_dis=comus_dis)
                serializer = ComusRCHSerializer(rch, data=request.data, partial=True)
            except ComusRCHModel.DoesNotExist:
                pass
            if serializer.is_valid():
                try:
                    period = ComusPeriodModel.objects.get(comus_dis=comus_dis)
                    period_count = len(period.period.keys())
                except ComusPeriodModel.DoesNotExist:
                    return Response({'error': 'ComusPeriodModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)
                try:
                    ctrl_pars = ComusCtrlParsModel.objects.get(comus_dis=comus_dis)
                    num_lyr = ctrl_pars.num_layer
                    num_row = ctrl_pars.num_row
                    num_col = ctrl_pars.num_col
                    data = request.data.get('data')
                    rech = request.data.get('rech')
                    try:
                        key_int = int(rech)
                        if key_int not in (1, 2):
                            return f"'rech' is out of range (1,2)"
                    except ValueError:
                        return f"'rech' is not an integer"
                    data_error = validate_values(data, num_lyr, num_row, num_col, 4, period_count)
                    if data_error:
                        return Response({"error": f"Invalid 'data' values: {data_error}"},
                                        status=status.HTTP_400_BAD_REQUEST)

                except ComusCtrlParsModel.DoesNotExist:
                    return Response({'error': 'ComusCtrlParsModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)
                serializer.save(comus_dis=comus_dis)
                if 'rch' in locals():
                    message = 'COMUS RCH parameters updated successfully'
                else:
                    message = 'COMUS RCH parameters saved successfully'
                return Response({'message': message}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (ComusDisModel.DoesNotExist):
            return Response({'error': 'This COMUS model not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            rch = ComusRCHModel.objects.get(comus_dis=comus_dis)
            rch.delete()
            return Response({'success': 'COMUS RCH parameters deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)
        except (ComusDisModel.DoesNotExist, ComusRCHModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its RCH parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)


class ComusWELView(APIView):
    def get(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            wel = ComusWELModel.objects.get(comus_dis=comus_dis)
            serializer = ComusWELSerializer(wel)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ComusDisModel.DoesNotExist, ComusWELModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its WEL parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = ComusWELSerializer(data=request.data)
        user_name = request.data.get('user_name')
        project_name = request.data.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            try:
                wel = ComusWELModel.objects.get(comus_dis=comus_dis)
                serializer = ComusWELSerializer(wel, data=request.data, partial=True)
            except ComusWELModel.DoesNotExist:
                pass
            if serializer.is_valid():
                try:
                    period = ComusPeriodModel.objects.get(comus_dis=comus_dis)
                    period_count = len(period.period.keys())
                except ComusPeriodModel.DoesNotExist:
                    return Response({'error': 'ComusPeriodModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)
                try:
                    ctrl_pars = ComusCtrlParsModel.objects.get(comus_dis=comus_dis)
                    num_lyr = ctrl_pars.num_layer
                    num_row = ctrl_pars.num_row
                    num_col = ctrl_pars.num_col
                    data = request.data.get('data')
                    data_error = validate_values(data, num_lyr, num_row, num_col, 5, period_count)
                    if data_error:
                        return Response({"error": f"Invalid 'data' values: {data_error}"},
                                        status=status.HTTP_400_BAD_REQUEST)

                except ComusCtrlParsModel.DoesNotExist:
                    return Response({'error': 'ComusCtrlParsModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)
                serializer.save(comus_dis=comus_dis)
                if 'wel' in locals():
                    message = 'COMUS WEL parameters updated successfully'
                else:
                    message = 'COMUS WEL parameters saved successfully'
                return Response({'message': message}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (ComusDisModel.DoesNotExist):
            return Response({'error': 'This COMUS model not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')

        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            wel = ComusWELModel.objects.get(comus_dis=comus_dis)
            wel.delete()
            return Response({'success': 'COMUS WEL parameters deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)
        except (ComusDisModel.DoesNotExist, ComusWELModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its WEL parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)


class ComusDRNView(APIView):
    def get(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            drn = ComusDRNModel.objects.get(comus_dis=comus_dis)
            serializer = ComusDRNSerializer(drn)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ComusDisModel.DoesNotExist, ComusDRNModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its DRN parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = ComusDRNSerializer(data=request.data)
        user_name = request.data.get('user_name')
        project_name = request.data.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            try:
                drn = ComusDRNModel.objects.get(comus_dis=comus_dis)
                serializer = ComusDRNSerializer(drn, data=request.data, partial=True)
            except ComusDRNModel.DoesNotExist:
                pass
            if serializer.is_valid():
                try:
                    period = ComusPeriodModel.objects.get(comus_dis=comus_dis)
                    period_count = len(period.period.keys())
                except ComusPeriodModel.DoesNotExist:
                    return Response({'error': 'ComusPeriodModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)
                try:
                    ctrl_pars = ComusCtrlParsModel.objects.get(comus_dis=comus_dis)
                    num_lyr = ctrl_pars.num_layer
                    num_row = ctrl_pars.num_row
                    num_col = ctrl_pars.num_col
                    data = request.data.get('data')
                    data_error = validate_values(data, num_lyr, num_row, num_col, 5, period_count)
                    if data_error:
                        return Response({"error": f"Invalid 'data' values: {data_error}"},
                                        status=status.HTTP_400_BAD_REQUEST)

                except ComusCtrlParsModel.DoesNotExist:
                    return Response({'error': 'ComusCtrlParsModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)
                serializer.save(comus_dis=comus_dis)
                if 'drn' in locals():
                    message = 'COMUS DRN parameters updated successfully'
                else:
                    message = 'COMUS DRN parameters saved successfully'
                return Response({'message': message}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (ComusDisModel.DoesNotExist):
            return Response({'error': 'This COMUS model not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            drn = ComusDRNModel.objects.get(comus_dis=comus_dis)
            drn.delete()
            return Response({'success': 'COMUS DRN parameters deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)
        except (ComusDisModel.DoesNotExist, ComusDRNModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its DRN parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)


class ComusEVTView(APIView):
    def get(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            evt = ComusEVTModel.objects.get(comus_dis=comus_dis)
            serializer = ComusEVTSerializer(evt)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ComusDisModel.DoesNotExist, ComusEVTModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its EVT parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = ComusEVTSerializer(data=request.data)
        user_name = request.data.get('user_name')
        project_name = request.data.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            try:
                shb = ComusEVTModel.objects.get(comus_dis=comus_dis)
                serializer = ComusEVTSerializer(shb, data=request.data, partial=True)
            except ComusEVTModel.DoesNotExist:
                pass
            if serializer.is_valid():
                try:
                    period = ComusPeriodModel.objects.get(comus_dis=comus_dis)
                    period_count = len(period.period.keys())
                except ComusPeriodModel.DoesNotExist:
                    return Response({'error': 'ComusPeriodModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)
                try:
                    ctrl_pars = ComusCtrlParsModel.objects.get(comus_dis=comus_dis)
                    num_lyr = ctrl_pars.num_layer
                    num_row = ctrl_pars.num_row
                    num_col = ctrl_pars.num_col
                    data = request.data.get('data')
                    data_error = validate_values(data, num_lyr, num_row, num_col, 7, period_count)
                    if data_error:
                        return Response({"error": f"Invalid 'data' values: {data_error}"},
                                        status=status.HTTP_400_BAD_REQUEST)

                except ComusCtrlParsModel.DoesNotExist:
                    return Response({'error': 'ComusCtrlParsModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)
                serializer.save(comus_dis=comus_dis)
                if 'evt' in locals():
                    message = 'COMUS EVT parameters updated successfully'
                else:
                    message = 'COMUS EVT parameters saved successfully'
                return Response({'message': message}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (ComusDisModel.DoesNotExist):
            return Response({'error': 'This COMUS model not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            evt = ComusEVTModel.objects.get(comus_dis=comus_dis)
            evt.delete()
            return Response({'success': 'COMUS EVT parameters deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)
        except (ComusDisModel.DoesNotExist, ComusEVTModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its EVT parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)


class ComusHFBView(APIView):
    def get(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            hfb = ComusHFBModel.objects.get(comus_dis=comus_dis)
            serializer = ComusHFBSerializer(hfb)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ComusDisModel.DoesNotExist, ComusHFBModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its HFB parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = ComusHFBSerializer(data=request.data)
        user_name = request.data.get('user_name')
        project_name = request.data.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            try:
                hfb = ComusHFBModel.objects.get(comus_dis=comus_dis)
                serializer = ComusHFBSerializer(hfb, data=request.data, partial=True)
            except ComusHFBModel.DoesNotExist:
                pass
            if serializer.is_valid():
                def validate_hfb_data(hfb_data, num_lyr, num_row, num_col):
                    if not isinstance(hfb_data, dict):
                        return f"'hfb_data' must be a dictionary."

                    for layer, values in hfb_data.items():
                        try:
                            layer_int = int(layer)
                            if layer_int < 1 or layer_int > num_lyr:
                                return f"Layer keys in 'hfb_data' must be integers between 1 and {num_lyr}."
                        except ValueError:
                            return f"Layer keys in 'hfb_data' must be integers."

                        if not isinstance(values, list):
                            return f"Each value in 'hfb_data' must be a list of lists."

                        for sublist in values:
                            if not isinstance(sublist, list) or len(sublist) != 5:
                                return f"Each sublist in 'hfb_data' must contain exactly 5 elements."
                            irow1, icol1, irow2, icol2, _ = sublist
                            if not (
                                    1 <= irow1 <= num_row and 1 <= icol1 <= num_col and 1 <= irow2 <= num_row and 1 <= icol2 <= num_col):
                                return f"Grid values must be between 1 and the respective num_row ({num_row}) or num_col ({num_col})."
                            if not ((abs(irow1 - irow2) == 1 and icol1 == icol2) or (
                                    abs(icol1 - icol2) == 1 and irow1 == irow2)):
                                return f"Cells must be adjacent in the grid for layer {layer}."

                    return None

                try:
                    ctrl_pars = ComusCtrlParsModel.objects.get(comus_dis=comus_dis)
                    num_lyr = ctrl_pars.num_layer
                    num_row = ctrl_pars.num_row
                    num_col = ctrl_pars.num_col
                    hfb_data = request.data.get('data')

                    hfb_error = validate_hfb_data(hfb_data, num_lyr, num_row, num_col)
                    if hfb_error:
                        return Response({"error": f"Invalid 'hfb_data' values: {hfb_error}"},
                                        status=status.HTTP_400_BAD_REQUEST)

                except ComusCtrlParsModel.DoesNotExist:
                    return Response({'error': 'ComusCtrlParsModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)
                serializer.save(comus_dis=comus_dis)
                if 'hfb' in locals():
                    message = 'COMUS HFB parameters updated successfully'
                else:
                    message = 'COMUS HFB parameters saved successfully'
                return Response({'message': message}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (ComusDisModel.DoesNotExist):
            return Response({'error': 'This COMUS model not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            hfb = ComusHFBModel.objects.get(comus_dis=comus_dis)
            hfb.delete()
            return Response({'success': 'COMUS HFB parameters deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)
        except (ComusDisModel.DoesNotExist, ComusHFBModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its HFB parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)


class ComusRIVView(APIView):
    def get(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            riv = ComusRIVModel.objects.get(comus_dis=comus_dis)
            serializer = ComusRIVSerializer(riv)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ComusDisModel.DoesNotExist, ComusRIVModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its RIV parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = ComusRIVSerializer(data=request.data)
        user_name = request.data.get('user_name')
        project_name = request.data.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            try:
                shb = ComusRIVModel.objects.get(comus_dis=comus_dis)
                serializer = ComusRIVSerializer(shb, data=request.data, partial=True)
            except ComusRIVModel.DoesNotExist:
                pass
            if serializer.is_valid():
                try:
                    period = ComusPeriodModel.objects.get(comus_dis=comus_dis)
                    period_count = len(period.period.keys())
                except ComusPeriodModel.DoesNotExist:
                    return Response({'error': 'ComusPeriodModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)
                try:
                    ctrl_pars = ComusCtrlParsModel.objects.get(comus_dis=comus_dis)
                    num_lyr = ctrl_pars.num_layer
                    num_row = ctrl_pars.num_row
                    num_col = ctrl_pars.num_col
                    data = request.data.get('data')
                    data_error = validate_values(data, num_lyr, num_row, num_col, 7, period_count)
                    if data_error:
                        return Response({"error": f"Invalid 'data' values: {data_error}"},
                                        status=status.HTTP_400_BAD_REQUEST)

                except ComusCtrlParsModel.DoesNotExist:
                    return Response({'error': 'ComusCtrlParsModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)
                serializer.save(comus_dis=comus_dis)
                if 'riv' in locals():
                    message = 'COMUS RIV parameters updated successfully'
                else:
                    message = 'COMUS RIV parameters saved successfully'
                return Response({'message': message}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (ComusDisModel.DoesNotExist):
            return Response({'error': 'This COMUS model not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            riv = ComusRIVModel.objects.get(comus_dis=comus_dis)
            riv.delete()
            return Response({'success': 'COMUS RIV parameters deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)
        except (ComusDisModel.DoesNotExist, ComusRIVModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its RIV parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)


class ComusIBSView(APIView):
    def get(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            ibs = ComusIBSModel.objects.get(comus_dis=comus_dis)
            serializer = ComusIBSSerializer(ibs)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ComusDisModel.DoesNotExist, ComusIBSModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its IBS parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = ComusIBSSerializer(data=request.data)
        user_name = request.data.get('user_name')
        project_name = request.data.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            try:
                shb = ComusIBSModel.objects.get(comus_dis=comus_dis)
                serializer = ComusIBSSerializer(shb, data=request.data, partial=True)
            except ComusIBSModel.DoesNotExist:
                pass
            if serializer.is_valid():
                def validate_ibs_data(data, num_lyr, num_row, num_col):
                    if not isinstance(data, dict):
                        return "'data' must be a dictionary."

                    for layer, values in data.items():
                        try:
                            layer_int = int(layer)
                            if layer_int < 1 or layer_int > num_lyr:
                                return f"Layer keys in 'data' must be integers between 1 and {num_lyr}."
                        except ValueError:
                            return f"Layer keys in 'data' must be integers."

                        if not isinstance(values, list):
                            return f"Each value in 'data' must be a list of lists."

                        for sublist in values:
                            if not isinstance(sublist, list) or len(sublist) != 6:
                                return f"Each sublist in 'data' must contain exactly 6 elements."
                            if not all(isinstance(x, (int, float)) for x in sublist):
                                return f"All elements in each sublist in 'data' must be numbers."
                            irow, icol, *rest = sublist
                            if not (1 <= irow <= num_row and 1 <= icol <= num_col):
                                return f"Row and column values must be between 1 and the respective num_row ({num_row}) or num_col ({num_col})."

                    return None

                try:
                    ctrl_pars = ComusCtrlParsModel.objects.get(comus_dis=comus_dis)
                    period = ComusPeriodModel.objects.get(comus_dis=comus_dis)
                    period_count = len(period.period.keys())
                    num_lyr = ctrl_pars.num_layer
                    num_row = ctrl_pars.num_row
                    num_col = ctrl_pars.num_col
                    data = request.data.get('data')
                    data_error = validate_ibs_data(data, num_lyr, num_row, num_col)
                    if data_error:
                        return Response({"error": f"Invalid 'data' values: {data_error}"},
                                        status=status.HTTP_400_BAD_REQUEST)


                except ComusCtrlParsModel.DoesNotExist:
                    return Response({'error': 'ComusCtrlParsModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)

                serializer.save(comus_dis=comus_dis)
                if 'ibs' in locals():
                    message = 'COMUS IBS parameters updated successfully'
                else:
                    message = 'COMUS IBS parameters saved successfully'
                return Response({'message': message}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (ComusDisModel.DoesNotExist):
            return Response({'error': 'This COMUS model not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            ibs = ComusIBSModel.objects.get(comus_dis=comus_dis)
            ibs.delete()
            return Response({'success': 'COMUS IBS parameters deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)
        except (ComusDisModel.DoesNotExist, ComusIBSModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its IBS parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)


class ComusSTRCtrlView(APIView):
    def get(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            str_ctrl = ComusSTRCtrlModel.objects.get(comus_dis=comus_dis)
            serializer = ComusSTRCtrlSerializer(str_ctrl)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ComusDisModel.DoesNotExist, ComusSTRCtrlModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its stream control parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = ComusSTRCtrlSerializer(data=request.data)
        user_name = request.data.get('user_name')
        project_name = request.data.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            try:
                str_ctrl = ComusSTRCtrlModel.objects.get(comus_dis=comus_dis)
                serializer = ComusSTRCtrlSerializer(str_ctrl, data=request.data, partial=True)
            except ComusSTRCtrlModel.DoesNotExist:
                pass
            if serializer.is_valid():
                serializer.save(comus_dis=comus_dis)
                if 'str_ctrl' in locals():
                    message = 'COMUS stream control parameters updated successfully'
                else:
                    message = 'COMUS stream control parameters saved successfully'
                return Response({'message': message}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (ComusDisModel.DoesNotExist):
            return Response({'error': 'This COMUS model not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            str_ctrl = ComusSTRCtrlModel.objects.get(comus_dis=comus_dis)
            str_ctrl.delete()
            return Response({'success': 'COMUS stream control parameters deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)
        except (ComusDisModel.DoesNotExist, ComusSTRCtrlModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its stream control parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)


class ComusSTRPeriodView(APIView):
    def get(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            str_period = ComusSTRPeriodModel.objects.get(comus_dis=comus_dis)
            serializer = ComusSTRPeriodSerializer(str_period)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ComusDisModel.DoesNotExist, ComusSTRPeriodModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its stream period parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = ComusSTRPeriodSerializer(data=request.data)
        user_name = request.data.get('user_name')
        project_name = request.data.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            try:
                str_period = ComusSTRPeriodModel.objects.get(comus_dis=comus_dis)
                serializer = ComusSTRPeriodSerializer(str_period, data=request.data, partial=True)
            except ComusSTRPeriodModel.DoesNotExist:
                pass
            if serializer.is_valid():
                try:
                    period = ComusPeriodModel.objects.get(comus_dis=comus_dis)
                    period_count = len(period.period.keys())
                except ComusPeriodModel.DoesNotExist:
                    return Response({'error': 'ComusPeriodModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)
                try:
                    str_ctrl_pars = ComusSTRCtrlModel.objects.get(comus_dis=comus_dis)
                    str_count = len(str_ctrl_pars.data.keys())
                except ComusSTRCtrlModel.DoesNotExist:
                    return Response({'error': 'ComusSTRCtrlModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)
                data = request.data.get('data')
                if not isinstance(data, dict):
                    return Response({'error': "The 'data' field must be a dictionary."},
                                    status=status.HTTP_400_BAD_REQUEST)
                for outer_key in data.keys():
                    if not (outer_key.isdigit() and 1 <= int(outer_key) <= str_count):
                        return Response(
                            {
                                'error': f"Each key in the outer dictionary must be a string representing an integer between 1 and {str_count}."},
                            status=status.HTTP_400_BAD_REQUEST)
                for outer_key, inner_dict in data.items():
                    if not isinstance(inner_dict, dict):
                        return Response(
                            {'error': f"The value for key '{outer_key}' must be a dictionary."},
                            status=status.HTTP_400_BAD_REQUEST)
                    for inner_key, value in inner_dict.items():
                        if not (inner_key.isdigit() and 1 <= int(inner_key) <= period_count):
                            return Response(
                                {
                                    'error': f"Each key in the inner dictionary for key '{outer_key}' must be a string representing an integer between 1 and {period_count}."},
                                status=status.HTTP_400_BAD_REQUEST)
                        if not (isinstance(value, list) and len(value) == 12 and all(
                                isinstance(x, (int, float)) for x in value)):
                            return Response(
                                {
                                    'error': f"The value for key '{inner_key}' in the inner dictionary for key '{outer_key}' must be a list of 12 numbers."},
                                status=status.HTTP_400_BAD_REQUEST)
                serializer.save(comus_dis=comus_dis)
                if 'str_period' in locals():
                    message = 'COMUS stream period parameters updated successfully'
                else:
                    message = 'COMUS stream period parameters saved successfully'
                return Response({'message': message}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (ComusDisModel.DoesNotExist):
            return Response({'error': 'This COMUS model not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            str_period = ComusSTRPeriodModel.objects.get(comus_dis=comus_dis)
            str_period.delete()
            return Response({'success': 'COMUS stream period parameters deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)
        except (ComusDisModel.DoesNotExist, ComusSTRPeriodModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its stream period parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)


class ComusSTRGridView(APIView):
    def get(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            str_grid = ComusSTRGridModel.objects.get(comus_dis=comus_dis)
            serializer = ComusSTRGridSerializer(str_grid)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ComusDisModel.DoesNotExist, ComusSTRGridModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its stream grid parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = ComusSTRGridSerializer(data=request.data)
        user_name = request.data.get('user_name')
        project_name = request.data.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            try:
                str_grid = ComusSTRGridModel.objects.get(comus_dis=comus_dis)
                serializer = ComusSTRGridSerializer(str_grid, data=request.data, partial=True)
            except ComusSTRGridModel.DoesNotExist:
                pass
            if serializer.is_valid():
                try:
                    str_ctrl_pars = ComusSTRCtrlModel.objects.get(comus_dis=comus_dis)
                    str_count = len(str_ctrl_pars.data.keys())
                except ComusSTRCtrlModel.DoesNotExist:
                    return Response({'error': 'ComusSTRCtrlModel not found for this COMUS model'},
                                    status=status.HTTP_400_BAD_REQUEST)
                try:
                    ctrl_pars = ComusCtrlParsModel.objects.get(comus_dis=comus_dis)
                    num_lyr = ctrl_pars.num_layer
                    num_row = ctrl_pars.num_row
                    num_col = ctrl_pars.num_col
                    data = request.data.get('data')
                    data_error = validate_values(data, num_lyr, num_row, num_col, 13, str_count)
                    if data_error:
                        return Response({"error": f"Invalid 'data' values: {data_error}"},
                                        status=status.HTTP_400_BAD_REQUEST)

                except ComusCtrlParsModel.DoesNotExist:
                    return Response({'error': 'ComusCtrlParsModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)
                serializer.save(comus_dis=comus_dis)
                if 'str_grid' in locals():
                    message = 'COMUS stream grid parameters updated successfully'
                else:
                    message = 'COMUS stream grid parameters saved successfully'
                return Response({'message': message}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (ComusDisModel.DoesNotExist):
            return Response({'error': 'This COMUS model not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            str_grid = ComusSTRGridModel.objects.get(comus_dis=comus_dis)
            str_grid.delete()
            return Response({'success': 'COMUS stream grid parameters deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)
        except (ComusDisModel.DoesNotExist, ComusSTRGridModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its stream grid parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)


class ComusSTRWaterUseView(APIView):
    def get(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            str_water_use = ComusSTRWaterUseModel.objects.get(comus_dis=comus_dis)
            serializer = ComusSTRWaterUseSerializer(str_water_use)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ComusDisModel.DoesNotExist, ComusSTRWaterUseModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its stream water use parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = ComusSTRWaterUseSerializer(data=request.data)
        user_name = request.data.get('user_name')
        project_name = request.data.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            try:
                str_water_use = ComusSTRWaterUseModel.objects.get(comus_dis=comus_dis)
                serializer = ComusSTRWaterUseSerializer(str_water_use, data=request.data, partial=True)
            except ComusSTRWaterUseModel.DoesNotExist:
                pass
            if serializer.is_valid():
                try:
                    ctrl_pars = ComusCtrlParsModel.objects.get(comus_dis=comus_dis)
                    num_lyr = ctrl_pars.num_layer
                    num_row = ctrl_pars.num_row
                    num_col = ctrl_pars.num_col
                    data = request.data.get('data')
                    if not isinstance(data, dict):
                        return Response({'error': "The 'data' field must be a dictionary."},
                                        status=status.HTTP_400_BAD_REQUEST)
                    for key in data.keys():
                        if not (key.isdigit() and 1 <= int(key) <= num_lyr):
                            return Response(
                                {
                                    'error': f"Each key in 'data' must be a string representing an integer between 1 and {num_lyr}."},
                                status=status.HTTP_400_BAD_REQUEST)
                    for key, value in data.items():
                        if not (isinstance(value, list) and all(
                                isinstance(item, list) and len(item) == 4 for item in value)):
                            return Response(
                                {
                                    'error': f"The value for key '{key}' must be a list of lists, each containing exactly 4 elements."},
                                status=status.HTTP_400_BAD_REQUEST)
                        for item in value:
                            if not (1 <= item[0] <= num_row):
                                return Response(
                                    {
                                        'error': f"The first element in each sublist for key '{key}' must be an integer between 1 and {num_row}."},
                                    status=status.HTTP_400_BAD_REQUEST)
                            if not (1 <= item[1] <= num_col):
                                return Response(
                                    {
                                        'error': f"The second element in each sublist for key '{key}' must be an integer between 1 and {num_col}."},
                                    status=status.HTTP_400_BAD_REQUEST)
                            if not all(isinstance(x, (int, float)) for x in item):
                                return Response(
                                    {
                                        'error': f"All elements in each sublist for key '{key}' must be integers or floats."},
                                    status=status.HTTP_400_BAD_REQUEST)

                except ComusCtrlParsModel.DoesNotExist:
                    return Response({'error': 'ComusCtrlParsModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)
                serializer.save(comus_dis=comus_dis)
                if 'str_water_use' in locals():
                    message = 'COMUS stream water use parameters updated successfully'
                else:
                    message = 'COMUS stream water use parameters saved successfully'
                return Response({'message': message}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (ComusDisModel.DoesNotExist):
            return Response({'error': 'This COMUS model not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            str_water_use = ComusSTRWaterUseModel.objects.get(comus_dis=comus_dis)
            str_water_use.delete()
            return Response({'success': 'COMUS stream water use parameters deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)
        except (ComusDisModel.DoesNotExist, ComusSTRWaterUseModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its stream water use parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)


class ComusSTRDrnView(APIView):
    def get(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            str_drn = ComusSTRDrnModel.objects.get(comus_dis=comus_dis)
            serializer = ComusSTRDrnSerializer(str_drn)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ComusDisModel.DoesNotExist, ComusSTRDrnModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its stream drainage parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = ComusSTRDrnSerializer(data=request.data)
        user_name = request.data.get('user_name')
        project_name = request.data.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            try:
                str_drn = ComusSTRDrnModel.objects.get(comus_dis=comus_dis)
                serializer = ComusSTRDrnSerializer(str_drn, data=request.data, partial=True)
            except ComusSTRDrnModel.DoesNotExist:
                pass
            if serializer.is_valid():
                try:
                    ctrl_pars = ComusCtrlParsModel.objects.get(comus_dis=comus_dis)
                    num_lyr = ctrl_pars.num_layer
                    num_row = ctrl_pars.num_row
                    num_col = ctrl_pars.num_col
                    data = request.data.get('data')
                    if not isinstance(data, dict):
                        return Response({'error': "The 'data' field must be a dictionary."},
                                        status=status.HTTP_400_BAD_REQUEST)
                    for key in data.keys():
                        if not (key.isdigit() and 1 <= int(key) <= num_lyr):
                            return Response(
                                {
                                    'error': f"Each key in 'data' must be a string representing an integer between 1 and {num_lyr}."},
                                status=status.HTTP_400_BAD_REQUEST)
                    for key, value in data.items():
                        if not (isinstance(value, list) and all(
                                isinstance(item, list) and len(item) == 5 for item in value)):
                            return Response(
                                {
                                    'error': f"The value for key '{key}' must be a list of lists, each containing exactly 5 elements."},
                                status=status.HTTP_400_BAD_REQUEST)
                        for item in value:
                            if not (1 <= item[0] <= num_row):
                                return Response(
                                    {
                                        'error': f"The first element in each sublist for key '{key}' must be an integer between 1 and {num_row}."},
                                    status=status.HTTP_400_BAD_REQUEST)
                            if not (1 <= item[1] <= num_col):
                                return Response(
                                    {
                                        'error': f"The second element in each sublist for key '{key}' must be an integer between 1 and {num_col}."},
                                    status=status.HTTP_400_BAD_REQUEST)
                            if not all(isinstance(x, (int, float)) for x in item):
                                return Response(
                                    {
                                        'error': f"All elements in each sublist for key '{key}' must be integers or floats."},
                                    status=status.HTTP_400_BAD_REQUEST)

                except ComusCtrlParsModel.DoesNotExist:
                    return Response({'error': 'ComusCtrlParsModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)
                serializer.save(comus_dis=comus_dis)
                if 'str_drn' in locals():
                    message = 'COMUS stream drainage parameters updated successfully'
                else:
                    message = 'COMUS stream drainage parameters saved successfully'
                return Response({'message': message}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (ComusDisModel.DoesNotExist):
            return Response({'error': 'This COMUS model not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            str_drn = ComusSTRDrnModel.objects.get(comus_dis=comus_dis)
            str_drn.delete()
            return Response({'success': 'COMUS stream drainage parameters deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)
        except (ComusDisModel.DoesNotExist, ComusSTRDrnModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its stream drainage parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)


class ComusRESCtrlView(APIView):
    def get(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            res_ctrl = ComusRESCtrlModel.objects.get(comus_dis=comus_dis)
            serializer = ComusRESCtrlSerializer(res_ctrl)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ComusDisModel.DoesNotExist, ComusRESCtrlModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its reservoir control parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = ComusRESCtrlSerializer(data=request.data)
        user_name = request.data.get('user_name')
        project_name = request.data.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            try:
                res_ctrl = ComusRESCtrlModel.objects.get(comus_dis=comus_dis)
                serializer = ComusRESCtrlSerializer(res_ctrl, data=request.data, partial=True)
            except ComusRESCtrlModel.DoesNotExist:
                pass
            if serializer.is_valid():
                serializer.save(comus_dis=comus_dis)
                if 'res_ctrl' in locals():
                    message = 'COMUS reservoir control parameters updated successfully'
                else:
                    message = 'COMUS reservoir control parameters saved successfully'
                return Response({'message': message}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (ComusDisModel.DoesNotExist):
            return Response({'error': 'This COMUS model not found'}, status=status.HTTP_404_NOT_FOUND)


class ComusRESPeriodView(APIView):
    def get(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            res_period = ComusRESPeriodModel.objects.get(comus_dis=comus_dis)
            serializer = ComusRESPeriodSerializer(res_period)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ComusDisModel.DoesNotExist, ComusRESPeriodModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its reservoir period parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = ComusRESPeriodSerializer(data=request.data)
        user_name = request.data.get('user_name')
        project_name = request.data.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            try:
                res_period = ComusRESPeriodModel.objects.get(comus_dis=comus_dis)
                serializer = ComusRESPeriodSerializer(res_period, data=request.data, partial=True)
            except ComusRESPeriodModel.DoesNotExist:
                pass
            if serializer.is_valid():
                try:
                    period = ComusPeriodModel.objects.get(comus_dis=comus_dis)
                    period_count = len(period.period.keys())
                except ComusPeriodModel.DoesNotExist:
                    return Response({'error': 'ComusPeriodModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)
                try:
                    res_ctrl_pars = ComusRESCtrlModel.objects.get(comus_dis=comus_dis)
                    res_count = len(res_ctrl_pars.data.keys())
                except ComusRESCtrlModel.DoesNotExist:
                    return Response({'error': 'ComusRESCtrlModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)
                data = request.data.get('data')
                if not isinstance(data, dict):
                    return Response({'error': "The 'data' field must be a dictionary."},
                                    status=status.HTTP_400_BAD_REQUEST)
                for outer_key in data.keys():
                    if not (outer_key.isdigit() and 1 <= int(outer_key) <= res_count):
                        return Response(
                            {
                                'error': f"Each key in the outer dictionary must be a string representing an integer between 1 and {res_count}."},
                            status=status.HTTP_400_BAD_REQUEST)
                for outer_key, inner_dict in data.items():
                    if not isinstance(inner_dict, dict):
                        return Response(
                            {'error': f"The value for key '{outer_key}' must be a dictionary."},
                            status=status.HTTP_400_BAD_REQUEST)
                    for inner_key, value in inner_dict.items():
                        if not (inner_key.isdigit() and 1 <= int(inner_key) <= period_count):
                            return Response(
                                {
                                    'error': f"Each key in the inner dictionary for key '{outer_key}' must be a string representing an integer between 1 and {period_count}."},
                                status=status.HTTP_400_BAD_REQUEST)
                        if not (isinstance(value, list) and len(value) == 4 and all(
                                isinstance(x, (int, float)) for x in value)):
                            return Response(
                                {
                                    'error': f"The value for key '{inner_key}' in the inner dictionary for key '{outer_key}' must be a list of 4 numbers."},
                                status=status.HTTP_400_BAD_REQUEST)
                serializer.save(comus_dis=comus_dis)
                if 'res_period' in locals():
                    message = 'COMUS reservoir period parameters updated successfully'
                else:
                    message = 'COMUS reservoir period parameters saved successfully'
                return Response({'message': message}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (ComusDisModel.DoesNotExist):
            return Response({'error': 'This COMUS model not found'}, status=status.HTTP_404_NOT_FOUND)


class ComusRESGridView(APIView):
    def get(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            res_grid = ComusRESGridModel.objects.get(comus_dis=comus_dis)
            serializer = ComusRESGridSerializer(res_grid)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ComusDisModel.DoesNotExist, ComusRESGridModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its reservoir grid parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = ComusRESGridSerializer(data=request.data)
        user_name = request.data.get('user_name')
        project_name = request.data.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            try:
                res_grid = ComusRESGridModel.objects.get(comus_dis=comus_dis)
                serializer = ComusRESGridSerializer(res_grid, data=request.data, partial=True)
            except ComusRESGridModel.DoesNotExist:
                pass
            if serializer.is_valid():
                try:
                    res_ctrl_pars = ComusRESCtrlModel.objects.get(comus_dis=comus_dis)
                    res_count = len(res_ctrl_pars.data.keys())
                except ComusRESCtrlModel.DoesNotExist:
                    return Response({'error': 'ComusRESCtrlModel not found for this COMUS model'},
                                    status=status.HTTP_400_BAD_REQUEST)
                try:
                    ctrl_pars = ComusCtrlParsModel.objects.get(comus_dis=comus_dis)
                    num_lyr = ctrl_pars.num_layer
                    num_row = ctrl_pars.num_row
                    num_col = ctrl_pars.num_col
                    data = request.data.get('data')
                    data_error = validate_values(data, num_lyr, num_row, num_col, 6, res_count)
                    if data_error:
                        return Response({"error": f"Invalid 'data' values: {data_error}"},
                                        status=status.HTTP_400_BAD_REQUEST)

                except ComusCtrlParsModel.DoesNotExist:
                    return Response({'error': 'ComusCtrlParsModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)

                serializer.save(comus_dis=comus_dis)
                if 'res_grid' in locals():
                    message = 'COMUS reservoir grid parameters updated successfully'
                else:
                    message = 'COMUS reservoir grid parameters saved successfully'
                return Response({'message': message}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (ComusDisModel.DoesNotExist):
            return Response({'error': 'This COMUS model not found'}, status=status.HTTP_404_NOT_FOUND)


class ComusLAKCtrlView(APIView):
    def get(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            lak_ctrl = ComusLAKCtrlModel.objects.get(comus_dis=comus_dis)
            serializer = ComusLAKCtrlSerializer(lak_ctrl)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ComusDisModel.DoesNotExist, ComusLAKCtrlModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its lake control parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = ComusLAKCtrlSerializer(data=request.data)
        user_name = request.data.get('user_name')
        project_name = request.data.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            try:
                lak_ctrl = ComusLAKCtrlModel.objects.get(comus_dis=comus_dis)
                serializer = ComusLAKCtrlSerializer(lak_ctrl, data=request.data, partial=True)
            except ComusLAKCtrlModel.DoesNotExist:
                pass
            if serializer.is_valid():
                serializer.save(comus_dis=comus_dis)
                if 'lak_ctrl' in locals():
                    message = 'COMUS lake control parameters updated successfully'
                else:
                    message = 'COMUS lake control parameters saved successfully'
                return Response({'message': message}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (ComusDisModel.DoesNotExist):
            return Response({'error': 'This COMUS model not found'}, status=status.HTTP_404_NOT_FOUND)


class ComusLAKPeriodView(APIView):
    def get(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            lak_period = ComusLAKPeriodModel.objects.get(comus_dis=comus_dis)
            serializer = ComusLAKPeriodSerializer(lak_period)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ComusDisModel.DoesNotExist, ComusLAKPeriodModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its lake period parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        user_name = request.data.get('user_name')
        project_name = request.data.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            try:
                lak_period = ComusLAKPeriodModel.objects.get(comus_dis=comus_dis)
                serializer = ComusLAKPeriodSerializer(lak_period, data=request.data, partial=True)
            except ComusLAKPeriodModel.DoesNotExist:
                serializer = ComusLAKPeriodSerializer(data=request.data)

            if serializer.is_valid():
                try:
                    period = ComusPeriodModel.objects.get(comus_dis=comus_dis)
                    period_count = len(period.period.keys())
                except ComusPeriodModel.DoesNotExist:
                    return Response({'error': 'ComusPeriodModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)
                try:
                    lak_ctrl_pars = ComusLAKCtrlModel.objects.get(comus_dis=comus_dis)
                    lak_count = len(lak_ctrl_pars.data.keys())
                except ComusLAKCtrlModel.DoesNotExist:
                    return Response({'error': 'ComusLAKCtrlModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)
                data = request.data.get('data')
                if not isinstance(data, dict):
                    return Response({'error': "The 'data' field must be a dictionary."},
                                    status=status.HTTP_400_BAD_REQUEST)
                for outer_key in data.keys():
                    if not (outer_key.isdigit() and 1 <= int(outer_key) <= lak_count):
                        return Response(
                            {
                                'error': f"Each key in the outer dictionary must be a string representing an integer between 1 and {lak_count}."},
                            status=status.HTTP_400_BAD_REQUEST)
                for outer_key, inner_dict in data.items():
                    if not isinstance(inner_dict, dict):
                        return Response(
                            {'error': f"The value for key '{outer_key}' must be a dictionary."},
                            status=status.HTTP_400_BAD_REQUEST)
                    for inner_key, value in inner_dict.items():
                        if not (inner_key.isdigit() and 1 <= int(inner_key) <= period_count):
                            return Response(
                                {
                                    'error': f"Each key in the inner dictionary for key '{outer_key}' must be a string representing an integer between 1 and {period_count}."},
                                status=status.HTTP_400_BAD_REQUEST)
                        if not (isinstance(value, list) and len(value) == 8 and all(
                                isinstance(x, (int, float)) for x in value)):
                            return Response(
                                {
                                    'error': f"The value for key '{inner_key}' in the inner dictionary for key '{outer_key}' must be a list of 8 numbers."},
                                status=status.HTTP_400_BAD_REQUEST)
                serializer.save(comus_dis=comus_dis)
                if 'lak_period' in locals():
                    message = 'COMUS lake period parameters updated successfully'
                else:
                    message = 'COMUS lake period parameters saved successfully'
                return Response({'message': message}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ComusDisModel.DoesNotExist:
            return Response({'error': 'This COMUS model not found'}, status=status.HTTP_404_NOT_FOUND)


class ComusLAKGridView(APIView):
    def get(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            lak_grid = ComusLAKGridModel.objects.get(comus_dis=comus_dis)
            serializer = ComusLAKGridSerializer(lak_grid)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ComusDisModel.DoesNotExist, ComusLAKGridModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its lake grid parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = ComusLAKGridSerializer(data=request.data)
        user_name = request.data.get('user_name')
        project_name = request.data.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            try:
                lak_grid = ComusLAKGridModel.objects.get(comus_dis=comus_dis)
                serializer = ComusLAKGridSerializer(lak_grid, data=request.data, partial=True)
            except ComusLAKGridModel.DoesNotExist:
                pass
            if serializer.is_valid():
                try:
                    lak_ctrl_pars = ComusLAKCtrlModel.objects.get(comus_dis=comus_dis)
                    lak_count = len(lak_ctrl_pars.data.keys())
                except ComusLAKCtrlModel.DoesNotExist:
                    return Response({'error': 'ComusLAKCtrlModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)
                try:
                    ctrl_pars = ComusCtrlParsModel.objects.get(comus_dis=comus_dis)
                    num_lyr = ctrl_pars.num_layer
                    num_row = ctrl_pars.num_row
                    num_col = ctrl_pars.num_col
                    data = request.data.get('data')
                    data_error = validate_values(data, num_lyr, num_row, num_col, 8, lak_count)
                    if data_error:
                        return Response({"error": f"Invalid 'data' values: {data_error}"},
                                        status=status.HTTP_400_BAD_REQUEST)

                except ComusCtrlParsModel.DoesNotExist:
                    return Response({'error': 'ComusCtrlParsModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)

                serializer.save(comus_dis=comus_dis)
                if 'lak_grid' in locals():
                    message = 'COMUS lake grid parameters updated successfully'
                else:
                    message = 'COMUS lake grid parameters saved successfully'
                return Response({'message': message}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (ComusDisModel.DoesNotExist):
            return Response({'error': 'This COMUS model not found'}, status=status.HTTP_404_NOT_FOUND)


class ComusREGView(APIView):
    def get(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            reg = ComusREGModel.objects.get(comus_dis=comus_dis)
            serializer = ComusREGSerializer(reg)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ComusDisModel.DoesNotExist, ComusREGModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its zone budget parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = ComusREGSerializer(data=request.data)
        user_name = request.data.get('user_name')
        project_name = request.data.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            try:
                reg = ComusREGModel.objects.get(comus_dis=comus_dis)
                serializer = ComusREGSerializer(reg, data=request.data, partial=True)
            except ComusREGModel.DoesNotExist:
                pass
            if serializer.is_valid():
                try:
                    ctrl_pars = ComusCtrlParsModel.objects.get(comus_dis=comus_dis)
                    num_lyr = ctrl_pars.num_layer
                    num_row = ctrl_pars.num_row
                    num_col = ctrl_pars.num_col
                    data = request.data.get('data')
                    for key, sub_dict in data.items():
                        if not isinstance(sub_dict, dict):
                            return Response({'error': f"The value for '{key}' must be a dictionary."},
                                            status=status.HTTP_400_BAD_REQUEST)
                        for sub_key, sub_value in sub_dict.items():
                            if not isinstance(sub_value, list):
                                return Response({'error': f"The value for '{sub_key}' must be a list of lists."},
                                                status=status.HTTP_400_BAD_REQUEST)
                            for item in sub_value:
                                if not (isinstance(item, list) and len(item) == 3):
                                    return Response(
                                        {'error': f"Each item in '{sub_key}' must be a list of three elements."},
                                        status=status.HTTP_400_BAD_REQUEST)
                                if not (1 <= item[0] <= num_lyr and 1 <= item[1] <= num_row and 1 <= item[
                                    2] <= num_col):
                                    return Response({'error': f"Elements in '{sub_key}' must be within valid range: "
                                                              f"1 <= lyr <= {num_lyr}, 1 <= row <= {num_row}, 1 <= col <= {num_col}."},
                                                    status=status.HTTP_400_BAD_REQUEST)
                except ComusCtrlParsModel.DoesNotExist:
                    return Response({'error': 'ComusCtrlParsModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)
                serializer.save(comus_dis=comus_dis)
                if 'reg' in locals():
                    message = 'COMUS zone budget parameters updated successfully'
                else:
                    message = 'COMUS zone budget parameters saved successfully'
                return Response({'message': message}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (ComusDisModel.DoesNotExist):
            return Response({'error': 'This COMUS model not found'}, status=status.HTTP_404_NOT_FOUND)


class ComusSUBCtrlView(APIView):
    def get(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            sub_ctrl = ComusSUBCtrlModel.objects.get(comus_dis=comus_dis)
            serializer = ComusSUBCtrlSerializer(sub_ctrl)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ComusDisModel.DoesNotExist, ComusSUBCtrlModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its subsidence control parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = ComusSUBCtrlSerializer(data=request.data)
        user_name = request.data.get('user_name')
        project_name = request.data.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            try:
                sub_ctrl = ComusSUBCtrlModel.objects.get(comus_dis=comus_dis)
                serializer = ComusSUBCtrlSerializer(sub_ctrl, data=request.data, partial=True)
            except ComusSUBCtrlModel.DoesNotExist:
                pass
            if serializer.is_valid():
                serializer.save(comus_dis=comus_dis)
                if 'sub_ctrl' in locals():
                    message = 'COMUS subsidence control parameters updated successfully'
                else:
                    message = 'COMUS subsidence control parameters saved successfully'
                return Response({'message': message}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (ComusDisModel.DoesNotExist):
            return Response({'error': 'This COMUS model not found'}, status=status.HTTP_404_NOT_FOUND)


class ComusSUBMzView(APIView):
    def get(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            sub_mz = ComusSUBMzModel.objects.get(comus_dis=comus_dis)
            serializer = ComusSUBMzSerializer(sub_mz)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ComusDisModel.DoesNotExist, ComusSUBMzModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its subsidence mz parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = ComusSUBMzSerializer(data=request.data)
        user_name = request.data.get('user_name')
        project_name = request.data.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            try:
                sub_mz = ComusSUBMzModel.objects.get(comus_dis=comus_dis)
                serializer = ComusSUBMzSerializer(sub_mz, data=request.data, partial=True)
            except ComusSUBMzModel.DoesNotExist:
                pass
            if serializer.is_valid():
                try:
                    sub_ctrl_pars = ComusSUBCtrlModel.objects.get(comus_dis=comus_dis)
                    mz_count = sub_ctrl_pars.num_mz
                    data = request.data.get('data')
                    if not isinstance(data, dict):
                        return Response({'error': "The 'data' field must be a dictionary."},
                                        status=status.HTTP_400_BAD_REQUEST)
                    for i in range(1, mz_count + 1):
                        key = str(i)
                        if key not in data:
                            return Response({'error': f"The 'data' field must include keys from '1' to '{mz_count}'."},
                                            status=status.HTTP_400_BAD_REQUEST)
                        value = data[key]
                        if not (isinstance(value, list) and len(value) == 3 and all(
                                isinstance(x, (int, float)) for x in value)):
                            return Response(
                                {'error': f"The value for key '{key}' must be a list of three numeric values."},
                                status=status.HTTP_400_BAD_REQUEST)
                except ComusSUBCtrlModel.DoesNotExist:
                    return Response({'error': 'ComusSUBCtrlModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)
                serializer.save(comus_dis=comus_dis)
                if 'sub_mz' in locals():
                    message = 'COMUS subsidence mz parameters updated successfully'
                else:
                    message = 'COMUS subsidence mz parameters saved successfully'
                return Response({'message': message}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (ComusDisModel.DoesNotExist):
            return Response({'error': 'This COMUS model not found'}, status=status.HTTP_404_NOT_FOUND)


class ComusSUBNdbLyrView(APIView):
    def get(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            sub_ndb_lyr = ComusSUBNdbLyrModel.objects.get(comus_dis=comus_dis)
            serializer = ComusSUBNdbLyrSerializer(sub_ndb_lyr)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ComusDisModel.DoesNotExist, ComusSUBNdbLyrModel.DoesNotExist):
            return Response(
                {'error': 'This COMUS model or its subsidence no delay interbeds layer parameters not found'},
                status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        user_name = request.data.get('user_name')
        project_name = request.data.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            try:
                sub_ndb_lyr = ComusSUBNdbLyrModel.objects.get(comus_dis=comus_dis)
                serializer = ComusSUBNdbLyrSerializer(sub_ndb_lyr, data=request.data, partial=True)
            except ComusSUBNdbLyrModel.DoesNotExist:
                serializer = ComusSUBNdbLyrSerializer(data=request.data)

            if serializer.is_valid():
                try:
                    ctrl_pars = ComusCtrlParsModel.objects.get(comus_dis=comus_dis)
                    num_lyr = ctrl_pars.num_layer
                except ComusCtrlParsModel.DoesNotExist:
                    return Response({'error': 'ComusCtrlParsModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)

                try:
                    sub_ctrl_pars = ComusSUBCtrlModel.objects.get(comus_dis=comus_dis)
                    ndb_lyr_count = sub_ctrl_pars.num_ndb
                    data = request.data.get('data')
                    if not isinstance(data, dict):
                        return Response({'error': "The 'data' field must be a dictionary."},
                                        status=status.HTTP_400_BAD_REQUEST)
                    expected_keys = {str(i) for i in range(1, ndb_lyr_count + 1)}
                    actual_keys = set(data.keys())
                    if expected_keys != actual_keys:
                        return Response({'error': f"The 'data' field must include keys from '1' to '{ndb_lyr_count}'."},
                                        status=status.HTTP_400_BAD_REQUEST)
                    for key, value in data.items():
                        if not (isinstance(value, int) and 1 <= value <= num_lyr):
                            return Response(
                                {'error': f"The value for key '{key}' must be an integer between 1 and {num_lyr}."},
                                status=status.HTTP_400_BAD_REQUEST)
                except ComusSUBCtrlModel.DoesNotExist:
                    return Response({'error': 'ComusSUBCtrlModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)
                serializer.save(comus_dis=comus_dis)
                if 'sub_ndb_lyr' in locals():
                    message = 'COMUS subsidence no delay interbeds layer parameters updated successfully'
                else:
                    message = 'COMUS subsidence no delay interbeds layer parameters saved successfully'
                return Response({'message': message}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ComusDisModel.DoesNotExist:
            return Response({'error': 'This COMUS model not found'}, status=status.HTTP_404_NOT_FOUND)


class ComusSUBNdbGridView(APIView):
    def get(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            sub_ndb_grid = ComusSUBNdbGridModel.objects.get(comus_dis=comus_dis)
            serializer = ComusSUBNdbGridSerializer(sub_ndb_grid)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ComusDisModel.DoesNotExist, ComusSUBNdbGridModel.DoesNotExist):
            return Response(
                {'error': 'This COMUS model or its subsidence no delay interbeds grid parameters not found'},
                status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        user_name = request.data.get('user_name')
        project_name = request.data.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            try:
                sub_ndb_grid = ComusSUBNdbGridModel.objects.get(comus_dis=comus_dis)
                serializer = ComusSUBNdbGridSerializer(sub_ndb_grid, data=request.data, partial=True)
            except ComusSUBNdbGridModel.DoesNotExist:
                serializer = ComusSUBNdbGridSerializer(data=request.data)

            if serializer.is_valid():
                try:
                    ctrl_pars = ComusCtrlParsModel.objects.get(comus_dis=comus_dis)
                    num_row = ctrl_pars.num_row
                    num_col = ctrl_pars.num_col
                except ComusCtrlParsModel.DoesNotExist:
                    return Response({'error': 'ComusCtrlParsModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)

                try:
                    sub_ctrl_pars = ComusSUBCtrlModel.objects.get(comus_dis=comus_dis)
                    ndb_lyr_count = sub_ctrl_pars.num_ndb
                    data = request.data.get('data')
                    if not isinstance(data, dict):
                        return Response({'error': "The 'data' field must be a dictionary."},
                                        status=status.HTTP_400_BAD_REQUEST)
                    for key in data.keys():
                        if not (key.isdigit() and 1 <= int(key) <= ndb_lyr_count):
                            return Response(
                                {
                                    'error': f"Each key in 'data' must be a string representing an integer between 1 and {ndb_lyr_count}."},
                                status=status.HTTP_400_BAD_REQUEST)
                    for key, value in data.items():
                        if not (isinstance(value, list) and all(
                                isinstance(item, list) and len(item) == 6 for item in value)):
                            return Response(
                                {
                                    'error': f"The value for key '{key}' must be a list of lists, each containing exactly 6 elements."},
                                status=status.HTTP_400_BAD_REQUEST)
                        for item in value:
                            if not (1 <= item[0] <= num_row):
                                return Response(
                                    {
                                        'error': f"The first element in each sublist for key '{key}' must be an integer between 1 and {num_row}."},
                                    status=status.HTTP_400_BAD_REQUEST)
                            if not (1 <= item[1] <= num_col):
                                return Response(
                                    {
                                        'error': f"The second element in each sublist for key '{key}' must be an integer between 1 and {num_col}."},
                                    status=status.HTTP_400_BAD_REQUEST)
                            if not all(isinstance(x, (int, float)) for x in item):
                                return Response(
                                    {
                                        'error': f"All elements in each sublist for key '{key}' must be integers or floats."},
                                    status=status.HTTP_400_BAD_REQUEST)
                except ComusSUBCtrlModel.DoesNotExist:
                    return Response({'error': 'ComusSUBCtrlModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)

                serializer.save(comus_dis=comus_dis)
                if 'sub_ndb_grid' in locals():
                    message = 'COMUS subsidence no delay interbeds grid parameters updated successfully'
                else:
                    message = 'COMUS subsidence no delay interbeds grid parameters saved successfully'
                return Response({'message': message}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ComusDisModel.DoesNotExist:
            return Response({'error': 'This COMUS model not found'}, status=status.HTTP_404_NOT_FOUND)


class ComusSUBDbLyrView(APIView):
    def get(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            sub_db_lyr = ComusSUBDbLyrModel.objects.get(comus_dis=comus_dis)
            serializer = ComusSUBDbLyrSerializer(sub_db_lyr)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ComusDisModel.DoesNotExist, ComusSUBDbLyrModel.DoesNotExist):
            return Response(
                {'error': 'This COMUS model or its subsidence delay interbeds layer parameters not found'},
                status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = ComusSUBDbLyrSerializer(data=request.data)
        user_name = request.data.get('user_name')
        project_name = request.data.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            try:
                sub_db_lyr = ComusSUBDbLyrModel.objects.get(comus_dis=comus_dis)
                serializer = ComusSUBDbLyrSerializer(sub_db_lyr, data=request.data, partial=True)
            except ComusSUBDbLyrModel.DoesNotExist:
                pass
            if serializer.is_valid():
                try:
                    ctrl_pars = ComusCtrlParsModel.objects.get(comus_dis=comus_dis)
                    num_lyr = ctrl_pars.num_layer
                except ComusCtrlParsModel.DoesNotExist:
                    return Response({'error': 'ComusCtrlParsModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)

                try:
                    sub_ctrl_pars = ComusSUBCtrlModel.objects.get(comus_dis=comus_dis)
                    db_lyr_count = sub_ctrl_pars.num_db
                    data = request.data.get('data')
                    if not isinstance(data, dict):
                        return Response({'error': "The 'data' field must be a dictionary."},
                                        status=status.HTTP_400_BAD_REQUEST)
                    expected_keys = {str(i) for i in range(1, db_lyr_count + 1)}
                    actual_keys = set(data.keys())
                    if expected_keys != actual_keys:
                        return Response({'error': f"The 'data' field must include keys from '1' to '{db_lyr_count}'."},
                                        status=status.HTTP_400_BAD_REQUEST)
                    for key, value in data.items():
                        if not (isinstance(value, int) and 1 <= value <= num_lyr):
                            return Response(
                                {'error': f"The value for key '{key}' must be an integer between 1 and {num_lyr}."},
                                status=status.HTTP_400_BAD_REQUEST)
                except ComusSUBCtrlModel.DoesNotExist:
                    return Response({'error': 'ComusSUBCtrlModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)
                serializer.save(comus_dis=comus_dis)
                if 'sub_db_lyr' in locals():
                    message = 'COMUS subsidence delay interbeds layer parameters updated successfully'
                else:
                    message = 'COMUS subsidence delay interbeds layer parameters saved successfully'
                return Response({'message': message}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (ComusDisModel.DoesNotExist):
            return Response({'error': 'This COMUS model not found'}, status=status.HTTP_404_NOT_FOUND)


class ComusSUBDbGridView(APIView):
    def get(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            sub_db_grid = ComusSUBDbGridModel.objects.get(comus_dis=comus_dis)
            serializer = ComusSUBDbGridSerializer(sub_db_grid)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ComusDisModel.DoesNotExist, ComusSUBDbGridModel.DoesNotExist):
            return Response(
                {'error': 'This COMUS model or its subsidence delay interbeds grid parameters not found'},
                status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = ComusSUBDbGridSerializer(data=request.data)
        user_name = request.data.get('user_name')
        project_name = request.data.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            try:
                sub_db_grid = ComusSUBDbGridModel.objects.get(comus_dis=comus_dis)
                serializer = ComusSUBDbGridSerializer(sub_db_grid, data=request.data, partial=True)
            except ComusSUBDbGridModel.DoesNotExist:
                pass
            if serializer.is_valid():
                try:
                    ctrl_pars = ComusCtrlParsModel.objects.get(comus_dis=comus_dis)
                    num_row = ctrl_pars.num_row
                    num_col = ctrl_pars.num_col
                except ComusCtrlParsModel.DoesNotExist:
                    return Response({'error': 'ComusCtrlParsModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)
                try:
                    sub_ctrl_pars = ComusSUBCtrlModel.objects.get(comus_dis=comus_dis)
                    db_lyr_count = sub_ctrl_pars.num_db
                    data = request.data.get('data')
                    if not isinstance(data, dict):
                        return Response({'error': "The 'data' field must be a dictionary."},
                                        status=status.HTTP_400_BAD_REQUEST)
                    for key in data.keys():
                        if not (key.isdigit() and 1 <= int(key) <= db_lyr_count):
                            return Response(
                                {
                                    'error': f"Each key in 'data' must be a string representing an integer between 1 and {db_lyr_count}."},
                                status=status.HTTP_400_BAD_REQUEST)
                    for key, value in data.items():
                        if not (isinstance(value, list) and all(
                                isinstance(item, list) and len(item) == 8 for item in value)):
                            return Response(
                                {
                                    'error': f"The value for key '{key}' must be a list of lists, each containing exactly 8 elements."},
                                status=status.HTTP_400_BAD_REQUEST)
                        for item in value:
                            if not (1 <= item[0] <= num_row):
                                return Response(
                                    {
                                        'error': f"The first element in each sublist for key '{key}' must be an integer between 1 and {num_row}."},
                                    status=status.HTTP_400_BAD_REQUEST)
                            if not (1 <= item[1] <= num_col):
                                return Response(
                                    {
                                        'error': f"The second element in each sublist for key '{key}' must be an integer between 1 and {num_col}."},
                                    status=status.HTTP_400_BAD_REQUEST)
                            if not all(isinstance(x, (int, float)) for x in item):
                                return Response(
                                    {
                                        'error': f"All elements in each sublist for key '{key}' must be integers or floats."},
                                    status=status.HTTP_400_BAD_REQUEST)
                except ComusSUBCtrlModel.DoesNotExist:
                    return Response({'error': 'ComusSUBCtrlModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)
                serializer.save(comus_dis=comus_dis)
                if 'sub_db_grid' in locals():
                    message = 'COMUS subsidence delay interbeds grid parameters updated successfully'
                else:
                    message = 'COMUS subsidence delay interbeds grid parameters saved successfully'
                return Response({'message': message}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (ComusDisModel.DoesNotExist):
            return Response({'error': 'This COMUS model not found'}, status=status.HTTP_404_NOT_FOUND)
