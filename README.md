## Cara Clone, Edit, dan Push Repository

1. Clone repository di branch dev dengan cara `git clone -b dev ttps://github.com/Syndrom2211/magang-alfian`
2. Di terminal, cek branch dengan cara `git branch`. Pastikan branch berada di `dev`
3. Cek origin dengan cara `git remote -v` dan pastikan kosong.
4. Setelah itu, Add atau set origin dengan `git remote set-url origin https://Syndrom2211:token@repository_ini` atau `git remote add origin https://Syndrom2211:token@https://github@repository_ini`
5. Edit kode dan setelah memodifikasi kode, lakukan `git add .`
6. Commit kode dengan `git commit -m "....."`
7. Push kode ke repository github dengan `git push`
8. Jika ada pesan error ketika push, lakukan `git push --set-upstream origin dev`
9. Setelah itu `git push`