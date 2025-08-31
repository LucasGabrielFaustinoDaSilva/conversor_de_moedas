// Seleciona os elementos do DOM
const deSelect = document.getElementById("de");
const paraSelect = document.getElementById("para");
const resultadoEl = document.getElementById("resultado");
const valorInput = document.getElementById("valor");
const botaoConverter = document.getElementById("converter");

// Função para carregar moedas do backend
async function carregarMoedas() {
    try {
        const response = await fetch("http://127.0.0.1:8001/moedas");
        const data = await response.json();

        // Verifica se houve erro
        if (data.error) {
            resultadoEl.textContent = "Erro ao carregar moedas: " + data.error;
            return;
        }

        // Limpar dropdowns
        deSelect.innerHTML = "";
        paraSelect.innerHTML = "";

        // Preencher dropdowns com código e nome
        for (const code in data) {
            const nome = data[code].description;
            deSelect.innerHTML += `<option value="${code}">${code} - ${nome}</option>`;
            paraSelect.innerHTML += `<option value="${code}">${code} - ${nome}</option>`;
        }

        // Valores padrão
        deSelect.value = "USD";
        paraSelect.value = "BRL";

    } catch (error) {
        console.error("Erro ao carregar moedas:", error);
        resultadoEl.textContent = "Erro ao conectar com o backend.";
    }
}

// Função para converter moeda
async function converterMoeda() {
    const de = deSelect.value;
    const para = paraSelect.value;
    const valor = parseFloat(valorInput.value);

    if (isNaN(valor) || valor <= 0) {
        resultadoEl.textContent = "Digite um valor válido para conversão.";
        return;
    }

    resultadoEl.textContent = "Carregando...";

    try {
        const response = await fetch(
            `http://127.0.0.1:8001/converter?de=${de}&para=${para}&valor=${valor}`
        );
        const data = await response.json();

        if (data.valor_convertido) {
            resultadoEl.textContent = `${valor} ${de} = ${data.valor_convertido.toFixed(2)} ${para}`;
        } else {
            resultadoEl.textContent = data.error || "Não foi possível converter.";
        }
    } catch (error) {
        resultadoEl.textContent = "Erro ao conectar com o backend.";
        console.error(error);
    }
}

// Eventos
window.addEventListener("load", carregarMoedas);
botaoConverter.addEventListener("click", converterMoeda);
