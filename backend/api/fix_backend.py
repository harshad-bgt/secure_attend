import os
path = r'E:\SecureAttend\backend\api\routes\attendance.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the overwrite bug!
old_block = '''        db.commit()
        qr_expires_at = session.qr_expires_at
    
    expires_in = int((qr_expires_at - now).total_seconds())'''

new_block = '''        db.commit()
        qr_expires_at = session.qr_expires_at
        if qr_expires_at and qr_expires_at.tzinfo is None:
            qr_expires_at = qr_expires_at.replace(tzinfo=timezone.utc)
    
    expires_in = int((qr_expires_at - now).total_seconds())'''

if old_block in content:
    content = content.replace(old_block, new_block)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Bug fixed!')
else:
    print('Block not found!')
