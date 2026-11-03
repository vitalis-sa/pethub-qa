"""
Cria no Azure Boards os Test Cases do plano de testes manuais do PetHub.

Cada caso de casos-de-teste.json vira um work item do tipo "Test Case" com:
  - Título:      "CT01 - Cadastro de tutor pelo site"
  - Description: objetivo, pré-condições, dados de entrada e saída esperada
  - Steps:       cada passo com Ação + Resultado esperado (aba Steps do Test Case)
  - Priority, Tags (PlanoDeTestes; Sprint 4; módulo) e, se informado, Iteration Path
  - Link "Tests" para o PBI correspondente, se você preencher o mapa de PBIs

Uso (PowerShell):
    $env:AZDO_PAT = "<seu Personal Access Token com escopo Work Items: Read & Write>"
    python importar_azure_boards.py --org RM565154 --project PetHub --iteration "PetHub\\Sprint 4"

Opções:
    --pbis pbis.json   arquivo {"CT01": 123, "CT02": 123, ...} com o ID do PBI testado
    --dry-run          mostra o que seria criado, sem chamar a API
Rodar de novo é seguro: casos cujo título já existe no projeto são pulados.
Só usa a biblioteca padrão do Python (3.8+).
"""
import argparse
import base64
import html
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "7.1"


def requisicao(metodo, url, pat, corpo=None, content_type="application/json"):
    token = base64.b64encode(f":{pat}".encode()).decode()
    dados = json.dumps(corpo).encode("utf-8") if corpo is not None else None
    req = urllib.request.Request(url, data=dados, method=metodo, headers={
        "Authorization": f"Basic {token}",
        "Content-Type": content_type,
        "Accept": "application/json",
    })
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detalhe = e.read().decode("utf-8", errors="replace")
        sys.exit(f"Erro {e.code} em {metodo} {url}\n{detalhe}")


def descricao_html(caso):
    linhas_entrada = "".join(
        f"<tr><td><b>{html.escape(k)}</b></td><td><code>{html.escape(v)}</code></td></tr>"
        for k, v in caso["entrada"].items())
    saidas = "".join(f"<li>{html.escape(s)}</li>" for s in caso["saida"])
    return (
        f"<p><b>Objetivo:</b> {html.escape(caso['objetivo'])}</p>"
        f"<p><b>Módulo:</b> {html.escape(caso['modulo'])}</p>"
        f"<p><b>Pré-condições:</b> {html.escape(caso['precondicoes'])}</p>"
        f"<p><b>Dados de entrada</b></p><table border='1' cellpadding='4'>{linhas_entrada}</table>"
        f"<p><b>Saída esperada</b></p><ul>{saidas}</ul>"
    )


def passos_xml(passos):
    """Formato do campo Microsoft.VSTS.TCM.Steps (HTML escapado dentro de XML)."""
    def bloco(texto):
        return html.escape(f"<DIV><P>{html.escape(texto)}</P></DIV>")

    itens = []
    for i, (acao, esperado) in enumerate(passos, start=2):
        itens.append(
            f'<step id="{i}" type="ValidateStep">'
            f'<parameterizedString isformatted="true">{bloco(acao)}</parameterizedString>'
            f'<parameterizedString isformatted="true">{bloco(esperado)}</parameterizedString>'
            f"<description/></step>")
    return f'<steps id="0" last="{len(passos) + 1}">{"".join(itens)}</steps>'


def titulos_existentes(base, pat):
    wiql = {"query": (
        "SELECT [System.Id] FROM WorkItems "
        "WHERE [System.TeamProject] = @project "
        "AND [System.WorkItemType] = 'Test Case' "
        "AND [System.Tags] CONTAINS 'PlanoDeTestes'")}
    res = requisicao("POST", f"{base}/_apis/wit/wiql?api-version={API}", pat, wiql)
    ids = [w["id"] for w in res.get("workItems", [])]
    titulos = set()
    for i in range(0, len(ids), 200):
        lote = ",".join(str(x) for x in ids[i:i + 200])
        itens = requisicao("GET", f"{base}/_apis/wit/workitems?ids={lote}"
                                  f"&fields=System.Title&api-version={API}", pat)
        titulos.update(w["fields"]["System.Title"] for w in itens["value"])
    return titulos


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--org", required=True, help="Organização, ex.: RM565154")
    p.add_argument("--project", required=True, help="Projeto, ex.: PetHub")
    p.add_argument("--iteration", help='Iteration Path, ex.: "PetHub\\Sprint 4"')
    p.add_argument("--area", help="Area Path (opcional)")
    p.add_argument("--pbis", help="JSON com o ID do PBI de cada caso")
    p.add_argument("--casos", default="casos-de-teste.json")
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()

    with open(a.casos, encoding="utf-8") as f:
        plano = json.load(f)
    mapa_pbi = {}
    if a.pbis:
        with open(a.pbis, encoding="utf-8") as f:
            mapa_pbi = json.load(f)

    org_url = f"https://dev.azure.com/{urllib.parse.quote(a.org)}"
    base = f"{org_url}/{urllib.parse.quote(a.project)}"

    pat = os.environ.get("AZDO_PAT", "")
    if not a.dry_run and not pat:
        sys.exit("Defina a variável de ambiente AZDO_PAT com o seu Personal Access Token.")

    existentes = set() if a.dry_run else titulos_existentes(base, pat)
    criados = 0
    for caso in plano["casos"]:
        titulo = f"{caso['id']} - {caso['titulo']}"
        if titulo in existentes:
            print(f"= {titulo} (já existe, pulado)")
            continue

        tags = f"PlanoDeTestes; {plano['sprint']}; {caso['modulo'].split(' - ')[0]}"
        ops = [
            {"op": "add", "path": "/fields/System.Title", "value": titulo},
            {"op": "add", "path": "/fields/System.Description", "value": descricao_html(caso)},
            {"op": "add", "path": "/fields/Microsoft.VSTS.TCM.Steps", "value": passos_xml(caso["passos"])},
            {"op": "add", "path": "/fields/Microsoft.VSTS.Common.Priority", "value": caso["prioridade"]},
            {"op": "add", "path": "/fields/System.Tags", "value": tags},
        ]
        if a.iteration:
            ops.append({"op": "add", "path": "/fields/System.IterationPath", "value": a.iteration})
        if a.area:
            ops.append({"op": "add", "path": "/fields/System.AreaPath", "value": a.area})
        pbi = mapa_pbi.get(caso["id"])
        if pbi:
            ops.append({"op": "add", "path": "/relations/-", "value": {
                "rel": "Microsoft.VSTS.Common.TestedBy-Reverse",
                "url": f"{org_url}/_apis/wit/workItems/{pbi}",
                "attributes": {"comment": "Caso de teste manual - Sprint 4"}}})

        if a.dry_run:
            print(f"+ {titulo}  [{len(caso['passos'])} passos, prioridade {caso['prioridade']}"
                  f"{', testa PBI ' + str(pbi) if pbi else ''}]")
            continue

        url = f"{base}/_apis/wit/workitems/$Test%20Case?api-version={API}"
        res = requisicao("POST", url, pat, ops, content_type="application/json-patch+json")
        criados += 1
        print(f"+ #{res['id']} {titulo}")

    if not a.dry_run:
        print(f"\n{criados} Test Case(s) criados. Veja em {base}/_workitems "
              f"(filtro: tag PlanoDeTestes).")


if __name__ == "__main__":
    main()
