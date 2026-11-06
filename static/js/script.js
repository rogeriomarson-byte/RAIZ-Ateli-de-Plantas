// RAIZ - JavaScript: usa Fetch para conversar com as rotas Flask (/api/...)

// Mostra uma mensagem rápida na parte de baixo da tela
function aviso(msg, erro = false) {
  const t = document.getElementById("toast");
  t.textContent = msg;
  t.className = "toast " + (erro ? "erro" : "") + " visivel";
  setTimeout(() => t.classList.remove("visivel"), 3500);
}

// Envia uma requisição para o servidor e devolve a resposta em JSON
async function api(url, metodo = "POST", corpo) {
  let r;
  try {
    r = await fetch(url, {
      method: metodo,
      headers: { "Content-Type": "application/json" },
      body: corpo ? JSON.stringify(corpo) : undefined,
    });
  } catch {
    throw new Error("Não foi possível falar com o servidor.");
  }
  const dados = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(dados.erro || "Erro inesperado.");
  return dados;
}

// Atualiza o número ao lado de "Carrinho"
function atualizarBadge(n) {
  const b = document.getElementById("badge");
  b.textContent = n;
  b.hidden = n === 0;
}

// Cliques em botões com data-acao
document.addEventListener("click", async (e) => {
  const b = e.target.closest("[data-acao]");
  if (!b) return;
  const id = b.dataset.id;
  try {
    if (b.dataset.acao === "adicionar") {
      const campo = document.getElementById("qtd-detalhe");
      const r = await api("/api/carrinho/adicionar", "POST", { planta_id: id, quantidade: campo ? campo.value : 1 });
      aviso(r.mensagem);
      atualizarBadge(r.qtd_total);
    } else if (b.dataset.acao === "remover-item") {
      await api("/api/carrinho/remover", "POST", { planta_id: id });
      location.reload();
    } else if (b.dataset.acao === "excluir") {
      if (!confirm("Tem certeza que deseja excluir?")) return;
      const r = await api(b.dataset.url, "DELETE");
      aviso(r.mensagem);
      setTimeout(() => location.reload(), 700);
    }
  } catch (err) {
    aviso(err.message, true);
  }
});

// Mudanças em campos: quantidade do carrinho e status do pedido
document.addEventListener("change", async (e) => {
  const el = e.target;
  try {
    if (el.classList.contains("qtd-carrinho")) {
      await api("/api/carrinho/alterar", "POST", { planta_id: el.dataset.id, quantidade: el.value });
      location.reload();
    } else if (el.classList.contains("status-pedido")) {
      const r = await api(`/api/admin/pedidos/${el.dataset.id}/status`, "PUT", { status: el.value });
      aviso(r.mensagem);
    }
  } catch (err) {
    aviso(err.message, true);
    if (el.classList.contains("qtd-carrinho")) setTimeout(() => location.reload(), 1200);
  }
});

// Envio dos formulários de contato e de finalizar pedido
document.addEventListener("submit", async (e) => {
  const f = e.target;
  if (f.id !== "form-contato" && f.id !== "form-pedido") return;
  e.preventDefault();
  try {
    const corpo = Object.fromEntries(new FormData(f));
    if (f.id === "form-contato") {
      const r = await api("/api/mensagens", "POST", corpo);
      aviso(r.mensagem);
      f.reset();
    } else {
      const r = await api("/api/pedidos", "POST", corpo);
      location.href = "/pedido/" + r.pedido_id;
    }
  } catch (err) {
    aviso(err.message, true);
  }
});
