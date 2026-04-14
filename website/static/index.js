function deleteStudent(studentId){
    fetch("/delete-student", {
        method: "POST",
        body: JSON.stringify({studentId: studentId})
    }).then((_res) => {
        window.location.href = "/"
    })
}

function deleteNilaiStudent(nilaiNisn){
    fetch("/delete-nilai-student", {
        method: "POST",
        body: JSON.stringify({nilaiNisn: nilaiNisn})
    }).then((_res) => {
        window.location.href = "/"
    })
}