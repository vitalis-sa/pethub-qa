# PetHub — Compliance, Quality Assurance & Tests (Sprint 4)

Equipe **Vitalis** · Challenge FIAP 2026 · empresa parceira CLYVO VET

## Entrega

| Item | Link |
|---|---|
| Plano de testes manuais (Azure DevOps) | [Test Plans do projeto `Sprint 4 – Azure DevOps`](https://dev.azure.com/RM565154/Sprint%204%20%E2%80%93%20Azure%20DevOps/_testPlans) |
| Backlog com os PBIs testados (Azure Boards) | [Backlog do projeto `Sprint 4 – Azure DevOps`](https://dev.azure.com/RM565154/Sprint%204%20%E2%80%93%20Azure%20DevOps/_backlogs) |
| Vídeo da automação (configuração, execução e resultados) | _cole aqui o link do YouTube (não listado)_ |
| Projeto Selenium IDE | [`automacao/PetHub.side`](automacao/PetHub.side) |

## Parte A — Testes manuais

O plano oficial está no Azure DevOps, organização `RM565154`, projeto `Sprint 4 – Azure DevOps`. São 64 *Test Cases*
agrupados em Test Plans por semana da release. Cada caso tem objetivo e pré-condições na descrição, passos com ação e
resultado esperado, parâmetros com os dados de entrada controlados e um link *Tests* para o PBI que valida.

A pasta `manual/` guarda um roteiro complementar de 24 casos de sistema (CT01 a CT24), escrito sobre as telas web
do pethub-java e a API Vitalis (.NET). Esses casos não foram importados no Azure.

- [`manual/casos-de-teste.json`](manual/casos-de-teste.json): fonte dos casos complementares
- [`manual/importar_azure_boards.py`](manual/importar_azure_boards.py): script que cria esses casos via API do Azure DevOps

| Bloco | Casos | Sistema sob teste |
|---|---|---|
| Autenticação e cadastro | CT01–CT04 | Web pethub-java (Thymeleaf) |
| Pets e segurança | CT05–CT07 | Web pethub-java |
| Consultas, prontuário e lembretes | CT08–CT14 | Web pethub-java |
| Responsável, endereços, contatos, lembretes, integração e health | CT15–CT23 | API Vitalis (.NET) |
| Wearable de hidratação (IoT) | CT24 | API pethub-java |

Massa de dados: `docs/seed_demo_video.sql` do repositório pethub-java (senha `123456`) + os valores fixos de cada caso.

## Parte B — Automação (Selenium IDE)

| Teste | Test Case no Azure | Caso complementar | O que valida |
|---|---|---|---|
| AT01 | 170 | CT03 | Login válido do tutor cai no painel e vê só o próprio pet |
| AT02 | 174 | CT04 | Senha errada mostra erro e não cria sessão |
| AT03 | sem caso no Azure | CT01 | Cadastro de tutor e primeiro login com a conta nova |
| AT04 | sem caso no Azure | CT05 | Cadastro de pet aparece no painel do tutor |
| AT05 | 183 | CT07 | Tutor recebe 403 ao abrir a área do veterinário |
| AT06 | 246 + 248 | CT08 + CT09 | Agendamento livre passa; mesmo horário é recusado |

### Como executar

1. Suba o pethub-java em `http://localhost:8080` com o seed carregado.
2. Instale a extensão **Selenium IDE** no Chrome ou Firefox.
3. Abra a extensão → *Open an existing project* → `automacao/PetHub.side`.
4. Selecione a suíte **Suite PetHub Web** e clique em *Run all tests in suite*.

AT03 e AT06 geram e-mail, CPF e horário únicos a cada execução, para a suíte poder rodar várias vezes
sem limpar o banco.
