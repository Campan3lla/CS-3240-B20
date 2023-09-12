var showForm = document.getElementById('id_account_type');
const studentForm = document.getElementById('id_student_form')
const advisorForm = document.getElementById('id_advisor_form')
$('#id_student_form').find('*').prop('disabled', true);
$('#id_advisor_form').find('*').prop('disabled', true);
showForm.addEventListener('change', function (event) {
        studentForm.style.display = 'none';

        advisorForm.style.display = 'none';


    const selector = showForm.value;

    if (selector === 'student') {
            $('#id_student_form').find('*').prop('disabled', false);
            studentForm.style.display = 'block';
        }
        else if (selector === 'advisor') {
            $('#id_advisor_form').find('*').prop('disabled', false);
            advisorForm.style.display = 'block';
        }
    }
);