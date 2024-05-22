from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ComusDisModel, ComusCtrlParsModel, ComusOutParsModel, ComusSpaceModel, ComusLpfPropModel, \
    ComusBcfPropModel, ComusGridParsModel, ComusPeriodModel
from .serializers import ComusModelSerializer, ComusCtrlParsSerializer, ComusOutParsSerializer, ComusSpaceSerializer, \
    ComusLpfPropSerializer, ComusBcfPropSerializer, ComusGridParsSerializer, ComusPeriodSerializer


class ComusModelView(APIView):
    def post(self, request):
        serializer = ComusModelSerializer(data=request.data)
        user_name = request.data.get('user_name')
        project_name = request.data.get('project_name')

        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'COMUS Model Created Successfully!'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')

        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            comus_dis.delete()
            return Response({'success': 'COMUS Model Deleted Successfully!'}, status=status.HTTP_204_NO_CONTENT)
        except ComusDisModel.DoesNotExist:
            return Response({'error': 'COMUS model not found'}, status=status.HTTP_404_NOT_FOUND)


class ComusCtrlParsView(APIView):
    def get(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            ctrl_pars = ComusCtrlParsModel.objects.get(comus_dis=comus_dis)
            serializer = ComusCtrlParsSerializer(ctrl_pars)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ComusDisModel.DoesNotExist, ComusCtrlParsModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its control parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = ComusCtrlParsSerializer(data=request.data)
        user_name = request.data.get('user_name')
        project_name = request.data.get('project_name')

        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            try:
                ctrl = ComusCtrlParsModel.objects.get(comus_dis=comus_dis)
                serializer = ComusCtrlParsSerializer(ctrl, data=request.data, partial=True)
            except ComusCtrlParsModel.DoesNotExist:
                pass
            if serializer.is_valid():
                serializer.save(comus_dis=comus_dis)
                if 'ctrl' in locals():
                    message = 'COMUS control parameters updated successfully'
                else:
                    message = 'COMUS control parameters saved successfully'
                return Response({'success': message}, status=status.HTTP_201_CREATED)
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
            comus_ctrl_pars = get_object_or_404(ComusCtrlParsModel, comus_dis=comus_dis)
            comus_ctrl_pars.delete()
            return Response({'success': 'COMUS control parameters deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)
        except ComusDisModel.DoesNotExist:
            return Response({'error': 'COMUS model not found'}, status=status.HTTP_404_NOT_FOUND)


class ComusOutParsView(APIView):
    def get(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')

        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            out_pars = ComusOutParsModel.objects.get(comus_dis=comus_dis)
            serializer = ComusOutParsSerializer(out_pars)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ComusDisModel.DoesNotExist, ComusOutParsModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its output parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = ComusOutParsSerializer(data=request.data)
        user_name = request.data.get('user_name')
        project_name = request.data.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            try:
                output = ComusOutParsModel.objects.get(comus_dis=comus_dis)
                serializer = ComusOutParsSerializer(output, data=request.data, partial=True)
            except ComusOutParsModel.DoesNotExist:
                pass
            if serializer.is_valid():
                serializer.save(comus_dis=comus_dis)
                if 'output' in locals():
                    message = 'COMUS output parameters updated successfully'
                else:
                    message = 'COMUS output parameters saved successfully'
                return Response({'success': message}, status=status.HTTP_201_CREATED)
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
            out_pars = ComusOutParsModel.objects.get(comus_dis=comus_dis)
            out_pars.delete()
            return Response({'success': 'COMUS output parameters deleted successfully'},
                            status=status.HTTP_204_NO_CONTENT)
        except (ComusDisModel.DoesNotExist, ComusOutParsModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its output parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)


class ComusSpaceView(APIView):
    def get(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')

        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            out_pars = ComusSpaceModel.objects.get(comus_dis=comus_dis)
            serializer = ComusSpaceSerializer(out_pars)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ComusDisModel.DoesNotExist, ComusSpaceModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its space parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = ComusSpaceSerializer(data=request.data)
        user_name = request.data.get('user_name')
        project_name = request.data.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            try:
                space = ComusSpaceModel.objects.get(comus_dis=comus_dis)
                serializer = ComusSpaceSerializer(space, data=request.data, partial=True)
            except ComusSpaceModel.DoesNotExist:
                pass

            if serializer.is_valid():
                try:
                    ctrl_pars = ComusCtrlParsModel.objects.get(comus_dis=comus_dis)
                    count = ctrl_pars.num_row + ctrl_pars.num_col
                    if not all([ctrl_pars.num_layer, ctrl_pars.num_row, ctrl_pars.num_col]):
                        return Response({'error': 'Some fields in ComusCtrlParsModel are missing'},
                                        status=status.HTTP_400_BAD_REQUEST)
                    if len(serializer.validated_data['data']['atti']) != count:
                        return Response({'error': f'Length of atti does not match with {count}'},
                                        status=status.HTTP_400_BAD_REQUEST)
                    num_ids = serializer.validated_data['data']['num_id']
                    if len(num_ids) != count:
                        return Response({'error': f'Length of num_id does not match with {count}'},
                                        status=status.HTTP_400_BAD_REQUEST)
                    for i, num_id in enumerate(num_ids):
                        if i < ctrl_pars.num_row:
                            if num_id != i + 1:
                                return Response({'error': 'Invalid num_id for row'},
                                                status=status.HTTP_400_BAD_REQUEST)
                        else:
                            if num_id != i - ctrl_pars.num_row + 1:
                                return Response({'error': 'Invalid num_id for column'},
                                                status=status.HTTP_400_BAD_REQUEST)
                except ComusCtrlParsModel.DoesNotExist:
                    return Response({'error': 'ComusCtrlParsModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)

                serializer.save(comus_dis=comus_dis)
                if 'space' in locals():
                    message = 'COMUS space parameters updated successfully'
                else:
                    message = 'COMUS space parameters saved successfully'
                return Response({'success': message}, status=status.HTTP_201_CREATED)
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
            space_pars = ComusSpaceModel.objects.get(comus_dis=comus_dis)
            space_pars.delete()
            return Response({'success': 'COMUS space parameters deleted successfully'},
                            status=status.HTTP_204_NO_CONTENT)
        except (ComusDisModel.DoesNotExist, ComusSpaceModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its space parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)


class ComusLpfPropView(APIView):
    def get(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            lpf_prop = ComusLpfPropModel.objects.get(comus_dis=comus_dis)
            serializer = ComusLpfPropSerializer(lpf_prop)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ComusDisModel.DoesNotExist, ComusLpfPropModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its LPF layer property parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = ComusLpfPropSerializer(data=request.data)
        user_name = request.data.get('user_name')
        project_name = request.data.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            try:
                lpf_prop = ComusLpfPropModel.objects.get(comus_dis=comus_dis)
                serializer = ComusLpfPropSerializer(lpf_prop, data=request.data, partial=True)
            except ComusLpfPropModel.DoesNotExist:
                pass

            if serializer.is_valid():
                try:
                    ctrl_pars = ComusCtrlParsModel.objects.get(comus_dis=comus_dis)
                    num_layer = ctrl_pars.num_layer

                    type_list = serializer.validated_data.get('data', {}).get('type', [])
                    cbd_list = serializer.validated_data.get('data', {}).get('cbd', [])
                    ibs_list = serializer.validated_data.get('data', {}).get('ibs', [])

                    if len(type_list) != num_layer or len(cbd_list) != num_layer or len(ibs_list) != num_layer:
                        return Response({'error': f'Length of type, cbd, and ibs should be {num_layer}'},
                                        status=status.HTTP_400_BAD_REQUEST)

                except ComusCtrlParsModel.DoesNotExist:
                    return Response({'error': 'ComusCtrlParsModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)

                serializer.save(comus_dis=comus_dis)
                if 'lpf_prop' in locals():
                    message = 'COMUS LPF layer property parameters updated successfully'
                else:
                    message = 'COMUS LPF layer property parameters saved successfully'
                return Response({'success': message}, status=status.HTTP_201_CREATED)
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
            lpf_prop = ComusLpfPropModel.objects.get(comus_dis=comus_dis)
            lpf_prop.delete()
            return Response({'success': 'COMUS LPF layer property parameters deleted successfully'},
                            status=status.HTTP_204_NO_CONTENT)
        except (ComusDisModel.DoesNotExist, ComusLpfPropModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its LPF layer property parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)


class ComusBcfPropView(APIView):
    def get(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            lpf_prop = ComusBcfPropModel.objects.get(comus_dis=comus_dis)
            serializer = ComusBcfPropSerializer(lpf_prop)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ComusDisModel.DoesNotExist, ComusBcfPropModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its BCF layer property parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = ComusBcfPropSerializer(data=request.data)
        user_name = request.data.get('user_name')
        project_name = request.data.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            try:
                bcf_prop = ComusBcfPropModel.objects.get(comus_dis=comus_dis)
                serializer = ComusBcfPropSerializer(bcf_prop, data=request.data, partial=True)
            except ComusBcfPropModel.DoesNotExist:
                pass

            if serializer.is_valid():
                try:
                    ctrl_pars = ComusCtrlParsModel.objects.get(comus_dis=comus_dis)
                    num_layer = ctrl_pars.num_layer

                    type_list = serializer.validated_data.get('data', {}).get('type', [])
                    trpy_list = serializer.validated_data.get('data', {}).get('trpy', [])
                    ibs_list = serializer.validated_data.get('data', {}).get('ibs', [])

                    if len(type_list) != num_layer or len(trpy_list) != num_layer or len(ibs_list) != num_layer:
                        return Response({'error': f'Length of type, trpy, and ibs should be {num_layer}'},
                                        status=status.HTTP_400_BAD_REQUEST)

                except ComusCtrlParsModel.DoesNotExist:
                    return Response({'error': 'ComusCtrlParsModel not found for this COMUS model'},
                                    status=status.HTTP_404_NOT_FOUND)

                serializer.save(comus_dis=comus_dis)
                if 'bcf_prop' in locals():
                    message = 'COMUS BCF layer property parameters updated successfully'
                else:
                    message = 'COMUS BCF layer property parameters saved successfully'
                return Response({'success': message}, status=status.HTTP_201_CREATED)
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
            bcf_prop = ComusBcfPropModel.objects.get(comus_dis=comus_dis)
            bcf_prop.delete()
            return Response({'success': 'COMUS BCF layer property parameters deleted successfully'},
                            status=status.HTTP_204_NO_CONTENT)
        except (ComusDisModel.DoesNotExist, ComusBcfPropModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its BCF layer property parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)


class ComusGridParsView(APIView):
    def get(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            grid_pars = ComusGridParsModel.objects.get(comus_dis=comus_dis)
            serializer = ComusGridParsSerializer(grid_pars)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ComusDisModel.DoesNotExist, ComusGridParsModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its grid parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        user_name = request.data.get('user_name')
        project_name = request.data.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            ctrl_pars = ComusCtrlParsModel.objects.get(comus_dis=comus_dis)
            if 'data' in request.data:
                for param_name in request.data['data']:
                    param_data = request.data['data'].get(param_name)
                    num_layer = ctrl_pars.num_layer
                    num_row = ctrl_pars.num_row
                    num_col = ctrl_pars.num_col
                    expected_length = num_layer * num_row * num_col
                    if param_data:
                        if not isinstance(param_data, list) or len(param_data) != expected_length:
                            return Response({'error': f"'{param_name}' should be a list with length {expected_length}"},
                                            status=status.HTTP_400_BAD_REQUEST)
                        for value in param_data:
                            if not isinstance(value, (int, float)):
                                return Response(
                                    {'error': f"All values in '{param_name}' should be integers or floats."},
                                    status=status.HTTP_400_BAD_REQUEST)
            serializer = ComusGridParsSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            try:
                grid_pars = ComusGridParsModel.objects.get(comus_dis=comus_dis)
                serializer = ComusGridParsSerializer(grid_pars, data=request.data, partial=True)
            except ComusGridParsModel.DoesNotExist:
                pass
            serializer.is_valid(raise_exception=True)
            serializer.save(comus_dis=comus_dis)
            if 'grid_pars' in locals():
                message = 'COMUS grid parameters updated successfully'
            else:
                message = 'COMUS grid parameters saved successfully'
            return Response({'success': message}, status=status.HTTP_201_CREATED)
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
            grid_pars = ComusGridParsModel.objects.get(comus_dis=comus_dis)
            grid_pars.delete()
            return Response({'success': 'COMUS grid parameters deleted successfully'},
                            status=status.HTTP_204_NO_CONTENT)
        except (ComusDisModel.DoesNotExist, ComusGridParsModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its grid parameters not found'},
                            status=status.HTTP_404_NOT_FOUND)


class ComusPeriodView(APIView):
    def get(self, request):
        user_name = request.query_params.get('user_name')
        project_name = request.query_params.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            out_pars = ComusPeriodModel.objects.get(comus_dis=comus_dis)
            serializer = ComusPeriodSerializer(out_pars)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ComusDisModel.DoesNotExist, ComusPeriodModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its period not found'},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = ComusPeriodSerializer(data=request.data)
        user_name = request.data.get('user_name')
        project_name = request.data.get('project_name')
        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
            try:
                ctrl = ComusPeriodModel.objects.get(comus_dis=comus_dis)
                serializer = ComusPeriodSerializer(ctrl, data=request.data, partial=True)
            except ComusPeriodModel.DoesNotExist:
                pass
            if serializer.is_valid():
                serializer.save(comus_dis=comus_dis)
                if 'ctrl' in locals():
                    message = 'COMUS period parameters updated successfully'
                else:
                    message = 'COMUS period parameters saved successfully'
                return Response({'success': message}, status=status.HTTP_201_CREATED)
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
            period = ComusPeriodModel.objects.get(comus_dis=comus_dis)
            period.delete()
            return Response({'success': 'COMUS period parameters deleted successfully'},
                            status=status.HTTP_204_NO_CONTENT)
        except (ComusDisModel.DoesNotExist, ComusPeriodModel.DoesNotExist):
            return Response({'error': 'This COMUS model or its period not found'}, status=status.HTTP_404_NOT_FOUND)
