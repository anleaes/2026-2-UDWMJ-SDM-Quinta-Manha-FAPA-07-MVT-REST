// ENIGMA - EscapeRoom | JavaScript geral do sistema.
// Um único arquivo, carregado com "defer" (não trava a abertura da página).

// Pede confirmação antes de excluir um registro.
// Uso: <a href="..." onclick="return confirmarExclusao()">Excluir</a>
function confirmarExclusao() {
  return confirm("Tem certeza que deseja excluir? Tudo que depende deste registro (ex.: jogos, horários e reservas de uma sala) também será excluído.");
}

document.addEventListener("DOMContentLoaded", function () {

  // 1) Menu lateral no celular (botão hambúrguer)
  var botaoMenu = document.getElementById("menu-toggle");
  if (botaoMenu) {
    botaoMenu.addEventListener("click", function () {
      document.body.classList.toggle("menu-open");
    });
    document.addEventListener("click", function (e) {
      if (document.body.classList.contains("menu-open") &&
          !e.target.closest(".sidebar") && !e.target.closest("#menu-toggle")) {
        document.body.classList.remove("menu-open");
      }
    });
  }

  // 2) Mensagens (toasts) somem sozinhas depois de 5 segundos
  document.querySelectorAll(".toast").forEach(function (toast) {
    function fechar() {
      toast.classList.add("is-leaving");
      setTimeout(function () { toast.remove(); }, 300);
    }
    var x = toast.querySelector(".close");
    if (x) { x.addEventListener("click", fechar); }
    setTimeout(fechar, 5000);
  });

  // 3) Filtros com data-autosubmit enviam o formulário ao mudar
  document.querySelectorAll("[data-autosubmit]").forEach(function (el) {
    el.addEventListener("change", function () { el.form.submit(); });
  });

  // 4) Máscaras simples (CPF e telefone) - só visual, a validação é do Django
  function soNumeros(v) { return v.replace(/\D/g, ""); }
  document.querySelectorAll("[data-mask='cpf']").forEach(function (el) {
    el.addEventListener("input", function () {
      var v = soNumeros(el.value).slice(0, 11);
      v = v.replace(/(\d{3})(\d)/, "$1.$2").replace(/(\d{3})(\d)/, "$1.$2").replace(/(\d{3})(\d{1,2})$/, "$1-$2");
      el.value = v;
    });
  });
  document.querySelectorAll("[data-mask='telefone']").forEach(function (el) {
    el.addEventListener("input", function () {
      var v = soNumeros(el.value).slice(0, 11);
      if (v.length > 10) { v = v.replace(/(\d{2})(\d{5})(\d{1,4})/, "($1) $2-$3"); }
      else if (v.length > 6) { v = v.replace(/(\d{2})(\d{4})(\d{1,4})/, "($1) $2-$3"); }
      else if (v.length > 2) { v = v.replace(/(\d{2})(\d{1,5})/, "($1) $2"); }
      el.value = v;
    });
  });

  // 5) Prévia da imagem escolhida no formulário
  document.querySelectorAll("input[type=file][accept^='image']").forEach(function (input) {
    input.addEventListener("change", function () {
      var antiga = input.parentNode.querySelector(".img-preview");
      if (antiga) { antiga.remove(); }
      if (input.files && input.files[0]) {
        var img = document.createElement("img");
        img.className = "img-preview";
        img.alt = "Prévia da imagem";
        img.src = URL.createObjectURL(input.files[0]);
        input.parentNode.appendChild(img);
      }
    });
  });
});
