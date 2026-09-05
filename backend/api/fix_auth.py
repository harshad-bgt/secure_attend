import os
path = r'E:\SecureAttend\backend\api\routes\auth.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

new_block = '''      elif hasattr(current_user, 'faculty_profile') and current_user.faculty_profile:
          profile["first_name"] = current_user.faculty_profile.first_name
          profile["last_name"] = current_user.faculty_profile.last_name
          
          # Add responsibilities
          profile["responsibilities"] = {"is_hod": False, "is_amc": False, "is_gfm": False}
          from database import SessionLocal
          from models import FacultyResponsibility
          db = SessionLocal()
          try:
              resp = db.query(FacultyResponsibility).filter_by(faculty_id=current_user.id).first()
              if resp:
                  profile["responsibilities"]["is_hod"] = resp.is_hod
                  profile["responsibilities"]["is_amc"] = resp.is_amc
                  profile["responsibilities"]["is_gfm"] = resp.is_gfm
          finally:
              db.close()
              
      return profile
'''
if 'profile["responsibilities"] =' not in content:
    content = content.replace("      return profile", new_block)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
