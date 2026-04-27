function deleteStudent(studentId){
    fetch("/delete-student", {
        method: "POST",
        body: JSON.stringify({studentId: studentId})
    }).then((_res) => {
        window.location.href = "/data-siswa"
    })
}

function deleteBerita(beritaId){
    fetch("/hapus-berita", {
        method: "POST",
        body: JSON.stringify({beritaId: beritaId})
    }).then((_res) => {
        window.location.href = "/"
    })
}

function deleteGuru(guruId){
    fetch("/hapus-data-guru", {
        method: "POST",
        body: JSON.stringify({guruId: guruId})
    }).then((_res) => {
        window.location.href = "/"
    })
}