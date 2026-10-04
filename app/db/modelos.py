"""Modelos de dados do Esteira LIE (SQLModel sobre SQLite).

Campos de lista (ex.: modalidades) são guardados como JSON em coluna texto nesta
fase, para manter o esquema simples. Use os utilitários em `repositorio.py`
(`ler_lista` / `guardar_lista`) para ler/gravar essas colunas.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class OSC(SQLModel, table=True):
    """Organização da Sociedade Civil proponente."""

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    cnpj: str = Field(index=True)
    # Endereço completo
    cep: Optional[str] = None
    logradouro: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    municipio: Optional[str] = None
    uf: Optional[str] = None
    # Dirigente
    dirigente_nome: Optional[str] = None
    dirigente_cargo: Optional[str] = None
    dirigente_cpf: Optional[str] = None  # opcional
    # Presença digital
    instagram: Optional[str] = None
    facebook_url: Optional[str] = None
    site: Optional[str] = None
    # Abrangência estatutária
    abrangencia_estatutaria: bool = False
    abrangencia_artigo_estatuto: Optional[str] = None
    observacoes: Optional[str] = None
    criada_em: datetime = Field(default_factory=datetime.now)


class ParceriaAnterior(SQLModel, table=True):
    """Histórico manual de parcerias/projetos anteriores da OSC.

    Inspirado no formulário de atestado do Ministério.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    osc_id: int = Field(foreign_key="osc.id", index=True)
    nome_projeto: str
    tipo: Optional[str] = None  # LIE | convênio | termo de fomento | termo de colaboração | outro
    numero_ano: Optional[str] = None
    orgao_parceiro: Optional[str] = None
    num_beneficiarios: Optional[int] = None
    atividades_realizadas: Optional[str] = None
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None
    estrutura_utilizada: Optional[str] = None
    qualificacao_equipe: Optional[str] = None


class ProfissionalEquipe(SQLModel, table=True):
    """Profissional da equipe técnica da OSC."""

    id: Optional[int] = Field(default=None, primary_key=True)
    osc_id: int = Field(foreign_key="osc.id", index=True)
    nome: str
    funcao: Optional[str] = None
    formacao: Optional[str] = None
    registro_profissional: Optional[str] = None  # ex.: CREF
    curriculo_arquivo: Optional[str] = None  # caminho local
    vinculo: Optional[str] = None


class Evidencia(SQLModel, table=True):
    """Evidência coletada ou enviada manualmente (base da rastreabilidade)."""

    id: Optional[int] = Field(default=None, primary_key=True)
    # Código de exibição, derivado do id (ex.: EV-0042); preenchido após o insert.
    codigo: Optional[str] = Field(default=None, index=True)
    osc_id: int = Field(foreign_key="osc.id", index=True)
    tipo: Optional[str] = None  # foto | vídeo | reportagem | publicação | post | site | ...
    origem: Optional[str] = None  # instagram | facebook | notícia | site | upload manual
    url_origem: Optional[str] = None
    data_do_fato: Optional[date] = None
    data_coleta: datetime = Field(default_factory=datetime.now)
    legenda: Optional[str] = None  # legenda/texto bruto
    caminho_arquivo: Optional[str] = None
    modalidades_json: Optional[str] = None  # lista em JSON
    tem_logomarca: str = "nao_verificado"  # sim | nao | nao_verificado
    tem_menores_identificaveis: str = "nao_verificado"  # sim | nao | nao_verificado
    status: str = "pendente"  # pendente | aprovada | descartada
    nota_curadoria: Optional[str] = None
    # Campos exigidos pelo Checklist CTO v3 (ver templates/ESTRUTURA_CTO.md):
    forma: Optional[str] = None  # link | print  (link é sempre preferível)
    eh_de_terceiros: str = "nao_verificado"  # sim | nao | nao_verificado (imprensa/órgão independente vale mais)
    mostra_pratica_esportiva: str = "nao_verificado"  # sim | nao | nao_verificado
    link_testado: str = "nao_verificado"  # sim | nao | nao_verificado (link quebrado é descartado)
    bloco_cto: Optional[str] = None  # 1 | 2 | 3 | 4 (bloco da CTO em que a evidência entra)


class Projeto(SQLModel, table=True):
    """Projeto esportivo em elaboração para uma OSC."""

    id: Optional[int] = Field(default=None, primary_key=True)
    osc_id: int = Field(foreign_key="osc.id", index=True)
    titulo: Optional[str] = None
    objeto: Optional[str] = None
    categoria_manifestacao: Optional[str] = None
    modalidades_json: Optional[str] = None
    local_execucao: Optional[str] = None
    publico_json: Optional[str] = None  # faixa etária, sexo, quantidade por núcleo/modalidade
    duracao_meses: Optional[int] = None
    criterios_selecao: Optional[str] = None
    # Status por seção, em JSON: {"objetivos": "rascunho", ...}
    status_secoes_json: Optional[str] = None
    criado_em: datetime = Field(default_factory=datetime.now)


class ItemOrcamento(SQLModel, table=True):
    """Item da planilha orçamentária de um projeto."""

    id: Optional[int] = Field(default=None, primary_key=True)
    projeto_id: int = Field(foreign_key="projeto.id", index=True)
    etapa: Optional[str] = None  # Atividade Fim | Atividade Meio | Elaboração e Captação | ...
    acao: Optional[str] = None
    descricao: Optional[str] = None
    unidade: Optional[str] = None
    quantidade: Optional[float] = None
    meses_ocorrencias: Optional[float] = None
    valor_unitario: Optional[float] = None
    origem_valor: Optional[str] = None  # catálogo | orçamento próprio | em branco
    memoria_calculo: Optional[str] = None
    justificativa: Optional[str] = None


class Regra(SQLModel, table=True):
    """Espelho da regra do regras.yaml, usado para guardar status e validação.

    O texto da regra permanece no regras.yaml (fonte da verdade). Esta tabela
    guarda principalmente o STATUS e a DATA DE VALIDAÇÃO feita pela Karine.
    """

    # Usa o id textual da regra (ex.: ORC-001) como chave primária.
    id: str = Field(primary_key=True)
    tema: Optional[str] = None
    descricao: Optional[str] = None
    tipo_checagem: Optional[str] = None
    fonte: Optional[str] = None
    vigencia: Optional[str] = None
    status: str = "pendente"  # pendente | validada | revogada
    data_validacao: Optional[datetime] = None
