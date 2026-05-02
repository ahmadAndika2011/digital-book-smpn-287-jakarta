function deleteStudent(studentId){
    if(confirm("Yakin hapus data Siswa? ")){
        fetch("/delete-student", {
            method: "POST",
            body: JSON.stringify({studentId: studentId})
        }).then((_res) => {
            window.location.href = "/data-siswa"
        })
    }
}

function deleteBerita(beritaId){
    if(confirm("Yakin hapus Berita")){
        fetch("/hapus-berita", {
            method: "POST",
            body: JSON.stringify({beritaId: beritaId})
        }).then((_res) => {
            window.location.href = "/berita"
        })
    }
}

function deleteGuru(guruId){
    if(confirm("Yakin hapus data Guru? ")){
        fetch("/hapus-data-guru", {
            method: "POST",
            body: JSON.stringify({guruId: guruId})
        }).then((_res) => {
            window.location.href = "/data-guru"
        })
    }
}

function deleteDataPpdb(dataPpdbId){
    if(confirm("Yakin hapus data PPDB? ")){
        fetch("/hapus-data-ppdb", {
            method: "POST",
            body: JSON.stringify({dataPpdbId: dataPpdbId})
        }).then((_res) => {
            window.location.href = "/dashbord-admin"
        })
    }
}

function deleteDataMutasi(dataMutasiId){
    if(confirm("Yakin hapus data Mutasi? ")){
        fetch("/hapus-data-mutasi", {
            method: "POST",
            body: JSON.stringify({dataMutasiId: dataMutasiId})
        }).then((_res) => {
            window.location.href = "/dashbord-admin"
        })
    }
}

function deleteDataPip(dataPipId){
    if(confirm("Yakin hapus data PIP? ")){
        fetch("/hapus-data-pip", {
            method: "POST",
            body: JSON.stringify({dataPipId: dataPipId})
        }).then((_res) => {
            window.location.href = "/dashbord-admin"
        })
    }
}

function deleteDataKjp(dataKjpId){
    if(confirm("Yakin Hapus Data KJP? ")){
        fetch("/hapus-data-kjp", {
            method: "POST",
            body: JSON.stringify({dataKjpId: dataKjpId})
        }).then((_res) => {
            window.location.href = "/dashbord-admin"
        })
    }
}

function deleteDataAdministrasiSekolah(dataAdministrasiSekolahId){
    if(confirm("Yakin hapus data layanan Administrasi Sekolah? ")){
        fetch("/hapus-data-administrasi-sekolah", {
            method: "POST",
            body: JSON.stringify({dataAdministrasiSekolahId: dataAdministrasiSekolahId})
        }).then((_res) => {
            window.location.href = "/dashbord-admin"
        })
    }
}

function deleteDataKunjunganAntarInstansi(dataKunjunganAntarInstansiId){
    if(confirm("Yakin hapus data Kunjungan Antar Instansi? ")){
        fetch("/hapus-data-kunjungan-antar-instansi", {
            method: "POST",
            body: JSON.stringify({dataKunjunganAntarInstansiId: dataKunjunganAntarInstansiId})
        }).then((_res) => {
            window.location.href = "/dashbord-admin"
        })
    }
}