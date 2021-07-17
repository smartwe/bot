import qrcode
from PIL import Image

iu_img = Image.open(r"C:\Users\spark\Desktop\kakaopy\KakaoBot\tests\qr\qrin.png")  # .crop((150, 40, 235, 150))

#썸내일 만들기
iu_img.thumbnail((60, 60))
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
qr.add_data("google.com")
qr.make()
iu_instagram = qr.make_image().convert('RGB')

#이미지 가운데 위치시키기
pos = ((iu_instagram.size[0] - iu_img.size[0]) // 2, (iu_instagram.size[1] - iu_img.size[1]) // 2)

iu_instagram.paste(iu_img, pos)
iu_instagram.save(r"C:\Users\spark\Desktop\kakaopy\KakaoBot\tests\qr\qr.png")
#print(iu_instagram.size)