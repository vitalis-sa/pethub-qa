# PetHub — Compliance, Quality Assurance & Tests (Sprint 4)

Equipe **Vitalis** · Challenge FIAP 2026 · empresa parceira CLYVO VET

## Entrega

| Item | Link |
|---|---|
| Plano de testes manuais (Azure Boards) | https://dev.azure.com/RM565154/PetHub/_workitems — filtro pela tag `PlanoDeTestes` |
| Vídeo da automação (configuração, execução e resultados) | _cole aqui o link do YouTube (não listado)_ |
| Projeto Selenium IDE | [`automacao/PetHub.side`](automacao/PetHub.side) |

## Parte A — Testes manuais

24 casos de teste de sistema (CT01–CT24) cadastrados como *Test Case* no Azure Boards, cada um com
objetivo, pré-condições, dados de entrada, saída esperada e passos (ação + resultado esperado).

- [`manual/casos-de-teste.json`](manual/casos-de-teste.json) — fonte dos casos
- [`manual/importar_azure_boards.py`](manual/importar_azure_boards.py) — cria os Test Cases via API do Azure DevOps

| Bloco | Casos | Sistema sob teste |
|---|---|---|
| Autenticação e cadastro | CT01–CT04 | Web pethub-java (Thymeleaf) |
| Pets e segurança | CT05–CT07 | Web pethub-java |
| Consultas, prontuário e lembretes | CT08–CT14 | Web pethub-java |
| Responsável, endereços, contatos, lembretes, integração e health | CT15–CT23 | API Vitalis (.NET) |
| Wearable de hidratação (IoT) | CT24 | API pethub-java |

Massa de dados: `docs/seed_demo_video.sql` do repositório pethub-java (senha `123456`) + os valores fixos de cada caso.

## Parte B — Automação (Selenium IDE)

| Teste | Caso manual | O que valida |
|---|---|---|
| AT01 | CT03 | Login válido do tutor cai no painel e vê só o próprio pet |
| AT02 | CT04 | Senha errada mostra erro e não cria sessão |
| AT03 | CT01 | Cadastro de tutor e primeiro login com a conta nova |
| AT04 | CT05 | Cadastro de pet aparece no painel do tutor |
| AT05 | CT07 | Tutor recebe 403 ao abrir a área do veterinário |
| AT06 | CT08 + CT09 | Agendamento livre passa; mesmo horário é recusado |

### Como executar

1. Suba o pethub-java em `http://localhost:8080` com o seed carregado.
2. Instale a extensão **Selenium IDE** no Chrome ou Firefox.
3. Abra a extensão → *Open an existing project* → `automacao/PetHub.side`.
4. Selecione a suíte **Suite PetHub Web** e clique em *Run all tests in suite*.

AT03 e AT06 geram e-mail, CPF e horário únicos a cada execução, para a suíte poder rodar várias vezes
sem limpar o banco.
