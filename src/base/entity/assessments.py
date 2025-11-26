'''
Author: Max great_maxwell@outlook.com
Date: 2025-11-26 14:43:34
LastEditors: Max great_maxwell@outlook.com
LastEditTime: 2025-11-26 14:58:52
FilePath: \Student-Wellbeing-System\src\base\entity\assessments.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

from dataclasses import dataclass

@dataclass
class Assessment:
    assessment_id:int
    student_id:int
    assignment_name:str
    grade:int
    submited_on_time:str
    