document.addEventListener('DOMContentLoaded', try_register)

function try_register() {
    let messages = Array.from(document.querySelectorAll('.errorlist'))
    let blocks = document.querySelectorAll('.error>input')

    blocks.forEach((item, idx) => {
        item.placeholder = messages[idx].innerText
        item.value = ''
        item.classList.add('rg_form-field-error')
        item.classList.remove('rg_form-field')
        item.addEventListener('click', () => {
            item.classList.remove('rg_form-field-error')
            item.classList.add('rg_form-field')
        })
        messages[idx].remove()
    })
}