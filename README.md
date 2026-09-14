## Features
- Personal profile
- Experience section
- Skills
- Projects
- Responsive desktop/mobile layout
- Semantic HTML5 structure
- Social media and Github links

## Tech Stack

- Python 3
- Django
- HTML5
- CSS3
- Git & GitHub

## Project Structure 

## Project Structure

```text
myportfolio/
├── main/
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   ├── 0002_project.py
│   │   └── 0003_alter_experience_category.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── portofolio/
│   ├── settings.py
│   ├── urls.py
│   └── views.py
├── static/
│   ├── css/
│   │   └── style.css
│   └── img/
├── templates/
│   ├── index.html
│   ├── experience.html
│   └── project.html
├── manage.py
├── requirements.txt
└── README.md
```

## Local Setup
### 1. Clone repository
git clone https://github.com/rachelinmiyuki/myportofolio.git 
cd myportofolio
### 2. Create virtual environment
python3 -m venv venv
### 3. Activate virtual environment
macOS/Linux:
source venv/bin/activate
Windows:
venv\Scripts\activate
### 4. Install dependencies
pip install -r requirements.txt
### 5. Run Django
python manage.py runserver

Website dapat diakses melalui:
http://localhost:8000/

## Development Progress
### Tutorial 0
- Membuat Django project.
- Menghubungkan repository dengan GitHub.
- Melakukan deployment awal ke PWS.

### Tutorial 1

- Membuat halaman profile.
- Menambahkan semantic HTML.
- Mengatur static files.
- Membuat responsive layout dasar.

### Tugas 1

- Menambahkan Experience, Skills, dan Projects section.
- Mengubah layout Experience, Skills, dan Projects menggunakan CSS Grid.
- Menambahkan media query untuk mobile.
- Menguji tampilan pada desktop dan mobile.
- Memperbaiki semantic HTML dan accessibility.
- Memperbarui dokumentasi dan AI disclosure.

### Tutorial 2

- Membuat Model, View, dan URL pada Django.
- Mengubah halaman Experience dari statis menjadi dinamis.
- Menghubungkan Model dengan database menggunakan migrations.
- Menggunakan Django Template untuk menampilkan data dari database.
- Mempelajari proses makemigrations dan migrate.
- Mengelola data melalui Django Admin.

### Tugas 2

- Merapikan isi Experience dan menambahkan gambar.
- Mengubah halaman Projects dari statis menjadi dinamis menggunakan Model, View, dan Template.
- Membuat model Project dan menghubungkannya dengan database.
- Menampilkan data Project secara dinamis dari database.
- Menambahkan fitur detail project melalui URL.
- Membuat testing untuk Model, View, dan halaman Project.
- Memperbarui dokumentasi dan AI disclosure.


### Refleksi Tugas 1

1. Iya, di website portofolio saya menggunakan beberapa elemen semantik HTML5 seperti <section> untuk membagi section utama pada website portofolio, yaitu about, experience, skills, dan projects. Menurut saya, penggunaan elemen ini cukup membantu karena struktur HTML jadi lebih jelas dan gampang dibaca. Saya juga jadi lebih mudah ketika ingin mengatur CSS untuk masing-masing bagian dikarenakan setiap section sudah punya fungsi yang jelas. Jadi walaupun website yang dibuat masih static, struktur kontennya tetap lebih terorganisir dan tidak hanya menggunakan <div> untuk semuanya.

2. Tantangan yang paling saya rasakan adalah saat menyesuaikan layout dari desktop ke mobile. Beberapa bagian yang di desktop terlihat rapih ternyata jadi kurang cocok ketika ukuran layar diperkecil, seeperti di section projects. Pada section projects, card  menggunakan swiper yang malah terlihat terlalu kurus di mobile karena ukurannya ikut mengecil. Hal tersebut menjadikan gambar dan teks di dalam card juga jadi lebih susah dibaca. Di section skills juga sempat ada masalah karena kotak-kotaknya jadi memanjang ke bawah satu per satu. Padahal menurut saya, akan lebih readable dan mempertahankan interest user lain jika tetap menggunakan bentuk 2x2, jadi informasinya tidak membuat halaman terlalu panjang dan tetap terlihat sebagai kumpulan skill. Setelah itu saya melihat responsive layout dari apakah semua elemennya muat di layar dan juga dan apakah bentuk dan informasi yang ditampilkan masih nyaman untuk dilihat. Maka dari itu, responsive menurut saya perlu menyesuaikan kembali susunan dan proporsinya supaya tetap readable oleh user di mobile maupun desktop.

3. Batasan yang saya rasakan dengan web portofolio yang masih berisfat static web adalah jika saya ingin mengubah atau menambah komponen tertentu pada section tertentu, saya harus mengubah kode nya lagi di html. Untuk development selanjutnya, saya berharap bisa menambahkan fungsi dinamis pada section projects, seperti melakukan filter pada tags projects yang ingin user seearch. Misalnya user hanya ingin tau projects saya yang berkaitan dengan Product Management, dan section projects hanya akan menampilkan proejcts yang berkaitan dengan itu. Selain itu, saya juga kepikiran untuk menambahkan experience dan projects secara manual di websitenya, seperti dengan menambahkan fitur button "+" or "add" agar saya sebagai admin tidak perlu bolak balik code untuk menambahan projek. Tentunya dengan saya sebagai admin pun akan membutuhkan skema login untuk akses yang terbatas (tidak sembarangan user bisa menjadi admin). Namun, saya menyadari bahwa development ini akan begitu kompleks hingga membutuhkan pemahaman backend.

AI disclosure: saya menggunakan AI berupa ChatGPT hanya untuk membantu saya dalam mencari alternatif dalam memecahkan masalah atau ketidaksesuaian tampilan website dengan keinginan saya. Saya tidak semena-mena copy paste, tetapi juga memahami mengapa perubahan pada suatu spesifik kode diperlukan. Strategi prompting yang saya lakukan bukan menumpahkan kode dan meminta AI menyelesaikan atau brainstorm sendiri, tetapi saya menanyakan kasus spesifik dan beberapa alternatif penyelesaiannya. Misalkan pada kasus tampilan swiper projects yang sempit di mobile, saya menanyakan bagaimana cara memastikan tampilan yang ada hanya 1 project setiap layar, dan AI menyarankan untuk menambahkan breakpoints serta penambahan case mobile di CSS. Setelah itu saya cerna terlebih dahulu maskudnya bagaimana dan saya eksperimenkan sesuai dengan yang saya butuhkan.

### Refleksi Tugas 2

1. Ketika user membuka halaman, request pertama masuk ke urls.py di level project. Dari sana, request diarahkan ke urls.py milik aplikasi yang sesuai. Setelah itu, urls.py aplikasi akan mengarahkan request ke view. Di dalam view, data yang dibutuhkan diambil dari model yang terhubung ke database. Data tersebut kemudian dikirim ke template. Template menggabungkan data dengan struktur HTML (project.html) yang sudah dibuat, lalu hasilnya dikirim kembali ke browser untuk ditampilkan.

2. Jika data ditulis langsung di template, setiap ada perubahan data kita harus mengubah kode HTML-nya juga (hard code). Jika sudah disimpan di model, data bisa diubah atau ditambah melalui database tanpa perlu mengubah struktur template. Maka dari itu, pemisahan antara data dan tampilan ini membuat aplikasi lebih mudah dirawat dan dikembangkan, terutama kalau jumlah data semakin banyak.

3. makemigrations digunakan untuk membuat berkas migration berdasarkan perubahan yang dilakukan pada model, yang belum diaplikasikan ke database. Sedangkan migrate digunakan untuk menerapkan perubahan model yang ada di berkas migrasi tersebut ke database. 

AI disclosure: Saya menggunakan AI berupa ChatGPT hanya untuk menanyakan alternatif dari beberapa masalah, seperti pada saat saya ingin memasukkan projects dan experience melalui terminal PWS yang setiap datanya membutuhkan link gambar, tetapi saya kesulitan dalam mengakses foto saya melalui link dan AI merekomendasikan saya menggunakan Cloudinary. Selain itu, saya juga menggunakan AI untuk membantu mencari tahu penyebab error pada saat melakukan testing, terutama ketika terdapat error karena self.experience tidak terbaca setelah saya menambahkan testing untuk Project.