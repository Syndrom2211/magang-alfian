## Cara Clone, Edit, dan Push Repository

1. Clone repository di branch dev dengan cara `git clone -b dev ttps://github.com/Syndrom2211/magang-alfian`
2. Buka projeknya dan lakukan `git init`
3. Add atau set origin dengan `git remote set-url origin https://Syndrom2211:token@repository_ini` atau `git remote add origin https://Syndrom2211:token@https://github@repository_ini`
4. Cek branch dengan cara `git branch`. Pastikan branch berada di `dev`
5. Pindah branch dengan cara `git branch dev`
6. Edit kode dan setelah memodifikasi kode, lakukan `git add .`
7. Commit kode dengan `git commit -m "....."`
8. Push kode ke repository github dengan `git push`
9. Jika ada pesan error ketika push, lakukan `git push --set-upstream origin dev`
10. Setelah itu `git push`