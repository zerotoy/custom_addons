import base64
import io
from odoo import models
from .excel_formatter import *

class VehicleReportXlsx(models.AbstractModel):
    _name = 'report.vehicle.report_vehicle_result_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, obj):
        row_rec = 0
        # self._define_formats(workbook)
        sheet = workbook.add_worksheet('Report Margin by Product')
        header1 = workbook.add_format(FONT_BIG_LEFT)
        header2 = workbook.add_format(FONT_BIG_BOLD_LEFT)
        header3 = workbook.add_format(FONT_BIG_BOLD_LEFT)
        header_table = workbook.add_format(TABLE_HEADER)
        table_content = workbook.add_format(TABLE_CONTENT)
        table_content_dec = workbook.add_format(TABLE_CONTENT_DEC)

        sheet.write(0, 2, 'Report Vehicle', header1)
        sheet.write(1, 2, 'Type', header2)
        sheet.write(1, 3, obj.type, header3)
        sheet.write(2, 2, 'Brand', header2)
        sheet.write(2, 3, obj.brand, header3)

        header = [
            'No.','Brand','Type','Model','Tahun','Price'
        ]
        column_sizes = [5,20, 20, 45, 22, 18]
        for col_num, col_size in enumerate(column_sizes):
            sheet.set_column(col_num, col_num, col_size)
        
        row_rec += 4

        for col_num, column_name in enumerate(header):
            sheet.write(row_rec, col_num, column_name, header_table)
    
        row_rec+=1
        num=0    
        for line in obj.line_ids:
            num += 1
            sheet.write(row_rec,0,num,table_content) #No.
            sheet.write(row_rec,1,line.brand_id,table_content) #Brand
            sheet.write(row_rec,2,line.type_id,table_content) #Type
            sheet.write(row_rec,3,line.model_id,table_content) #Model
            sheet.write(row_rec,4,line.year,table_content) #Tahun
            sheet.write(row_rec,5,line.price,table_content_dec) #Price
            row_rec+=1
        
        sheet.freeze_panes(5,0)
        sheet.set_zoom(80)
        