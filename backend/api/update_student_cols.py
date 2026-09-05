import os
path = r'E:\SecureAttend\backend\api\models.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

new_student_cols = '''    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"))
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    blood_group: Mapped[Optional[str]] = mapped_column(String(10))
    address: Mapped[Optional[str]] = mapped_column(Text)
    profile_photo_url: Mapped[Optional[str]] = mapped_column(String(500))
'''

if 'blood_group: Mapped' not in content:
    content = content.replace('    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"))\n', new_student_cols)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Added missing profile columns to Student')
else:
    print('Already added')
