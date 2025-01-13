WITH beneficios_agg AS (
    SELECT
        vb.vaga_id,
        STRING_AGG(b.nome, ', ') AS beneficios
    FROM
        vaga_beneficios vb
    JOIN
        beneficios b ON vb.beneficio_id = b.beneficio_id
    GROUP BY
        vb.vaga_id
),
requisitos_agg AS (
    SELECT
        vr.vaga_id,
        STRING_AGG(r.nome, ', ') AS requisitos
    FROM
        vaga_requisitos vr
    JOIN
        requisitos r ON vr.requisito_id = r.requisito_id
    GROUP BY
        vr.vaga_id
),
competencias_agg AS (
    SELECT
        vc.vaga_id,
        STRING_AGG(c.nome, ', ') AS competencias
    FROM
        vaga_competencias vc
    JOIN
        competencias c ON vc.competencia_id = c.competencia_id
    GROUP BY
        vc.vaga_id
)
select
	v.codigo_vaga,
	v.vaga_id,
    
	v.link_site,
	v.link_origem,
	v.data_publicacao,
	v.data_coleta,
    v.posicao,
    v.senioridade,
    v.titulo_vaga,
    e.nome_empresa,
    v.cidade,
    v.estado,
    v.modalidade,
    COALESCE(b.beneficios, '') AS beneficios,
    COALESCE(r.requisitos, '') AS requisitos,
    COALESCE(c.competencias, '') AS competencias
FROM
    vagas v
LEFT join
	empresas e on v.empresa_id = e.empresa_id 
LEFT JOIN
    beneficios_agg b ON v.vaga_id = b.vaga_id
LEFT JOIN
    requisitos_agg r ON v.vaga_id = r.vaga_id
LEFT JOIN
    competencias_agg c ON v.vaga_id = c.vaga_id
WHERE 
	v.estado = 'PR' 
	AND requisitos LIKE '%Power BI%'
	AND TO_DATE(v.data_coleta, 'YYYY-MM-DD') >= CURRENT_DATE - INTERVAL '2 days'
LIMIT 30;