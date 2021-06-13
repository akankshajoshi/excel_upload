from django.shortcuts import render
import xlrd
from django.db import transaction
from.models import *


def export_student(request):
    context = {}
    if request.method == 'POST':
        new_students = request.FILES['my_file']
        excel_type = new_students.name.split('.')[1]
        if excel_type in ['xlsx', 'xls']:
            wb = xlrd.open_workbook(filename=None, file_contents=new_students.read())
            table = wb.sheets()[0]
            rows = table.nrows  #
            cols = table.ncols
            if cols != 6:
                context.update({'error': 'The Columns are not appropiate'})
                return render(request, 'upload_student.html', context)
            try:
                no_valid_serial = []
                no_valid_email = []
                no_valid_contact = []

                # validate all values
                exist_serial = Student.objects.all().values_list('serial_no', flat=True)

                for i in range(1, rows):
                    _row_values = table.row_values(i)
                    if not _row_values[5] or not(validate_contact(_row_values[5])):
                        no_valid_contact.append(str(i))
                    if not _row_values[0]:
                        no_valid_serial.append(str(i))
                    elif _row_values[0] and int(_row_values[0]) in exist_serial:
                        no_valid_serial.append(str(i))
                    if not validate_emailid(_row_values[4]):
                        no_valid_email.append(str(i))
                context['error'] = ''
                err = ''
                if no_valid_serial:
                    err = 'The Serial Nos in rows %s are not Valid ' % (','.join(no_valid_serial))
                if no_valid_email:
                    if err:
                        err = err + ', The Email Ids in rows %s are not Valid ' % (','.join(no_valid_email))
                    else:
                        err = 'The Email Ids in rows %s are not Valid ' % (','.join(no_valid_email))
                if no_valid_contact:
                    if err:
                        err = err + ', The Contact in rows %s are not Valid ' %(','.join(no_valid_contact))
                    else:
                        err = 'The Contact in rows %s are not Valid ' % (','.join(no_valid_contact))
                if err:
                    context.update({'error': err})
                    return render(request, 'upload_student.html', context)
                with transaction.atomic():  # database transaction transaction control
                    for i in range(1, rows):
                        _row_values = table.row_values(i)
                        Student.objects.create(serial_no=int(_row_values[0]), first_name=_row_values[0], last_name=_row_values[2],
                                               email_id=_row_values[3], contact=_row_values[4])
                        context.update({'message': 'Import done successfully'})
            except:
                context.update({'error': 'Parse excel file or data insertion error'})
        else:
            context.update({'error': 'Upload file type error!'})
    return render(request, 'upload_student.html', context)


