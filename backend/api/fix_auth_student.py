import os
path = r'E:\SecureAttend\backend\api\routes\auth.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add phone, blood_group, address to /me
if 'profile["phone"] = current_user.student_profile.phone' not in content:
    old_block = '''          profile["student_id"] = current_user.student_profile.roll_number
          profile["face_profile_active"] = current_user.student_profile.face_profile_active'''
    new_block = '''          profile["student_id"] = current_user.student_profile.roll_number
          profile["face_profile_active"] = current_user.student_profile.face_profile_active
          profile["phone"] = current_user.student_profile.phone
          profile["blood_group"] = current_user.student_profile.blood_group
          profile["address"] = current_user.student_profile.address'''
    content = content.replace(old_block, new_block)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
