"""Projeto 01: CRUD de alunos por matricula."""
from datetime import datetime
from pymongo.errors import DuplicateKeyError
from conexao import banco

alunos = banco['alunos_p01']
alunos.create_index('matricula', unique=True)

while True:
    print('\n[1] Cadastrar [2] Listar [3] Buscar por Curso [4] Alterar [5] Excluir [0] Sair')
    opcao = input('Opção: ').strip()
    
    if opcao == '1':
        matricula = input('Matrícula: ').strip()
        nome = input('Nome: ').strip()
        curso = input('Curso: ').strip()
        if not all([matricula, nome, curso]):
            print('Preencha todos os campos.')
            continue
        
        # Gera a data e hora atual do sistema
        data_matricula = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        try:
            alunos.insert_one({
                'matricula': matricula, 
                'nome': nome, 
                'curso': curso,
                'data_matricula': data_matricula
            })
            print(f'Aluno cadastrado com sucesso em {data_matricula}!')
        except DuplicateKeyError:
            print('Matrícula já cadastrada.')
            
    elif opcao == '2':
        for aluno in alunos.find({}, {'_id': 0}).sort('nome', 1):
            print(aluno)
            
    elif opcao == '3':
        curso_procurado = input('Digite o nome do curso que deseja buscar: ').strip()
        encontrou = False
        print(f"\n--- Alunos do curso: {curso_procurado} ---")
        for aluno in alunos.find({'curso': curso_procurado}, {'_id': 0}).sort('nome', 1):
            print(f"Nome: {aluno.get('nome')} | Matrícula: {aluno.get('matricula')} | Data: {aluno.get('data_matricula', 'N/D')}")
            encontrou = True
        if not encontrou:
            print('Nenhum aluno encontrado neste curso.')
            
    elif opcao == '4':
        matricula = input('Matrícula: ').strip()
        novo_curso = input('Novo curso: ').strip()
        if novo_curso:
            r = alunos.update_one({'matricula': matricula}, {'$set': {'curso': novo_curso}})
            print('Atualizado!' if r.matched_count else 'Aluno não encontrado.')
            
    elif opcao == '5':
        matricula = input('Matrícula: ').strip()
        r = alunos.delete_one({'matricula': matricula})
        print('Excluído!' if r.deleted_count else 'Aluno não encontrado.')
        
    elif opcao == '0':
        break
        
    else:
        print('Opção inválida.')