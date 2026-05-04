import os, glob

def tr(filepath, replacements):
    win_path = filepath.replace('/n/', 'N:/')
    if not os.path.exists(win_path):
        return
    with open(win_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    changed = False
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            changed = True
    if changed:
        with open(win_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  OK: {os.path.basename(filepath)}")

B = '/n/Users/tinch/Documents/Projetos/ragnarok/npc'

# === HEALER ===
tr(f'{B}/custom/healer.txt', [
    ('"Healing costs "', '"A cura custa "'),
    ('"^0055FFHeal^000000:^777777Cancel^000000"', '"^0055FFCurar^000000:^777777Cancelar^000000"'),
])

# === BREEDER ===
tr(f'{B}/custom/breeder.txt', [
    ('"You must first remove your mount."', '"Voce precisa remover sua montaria primeiro."'),
    ('"You do not meet requirements to rent."', '"Voce nao atende os requisitos para alugar."'),
])

# === CARD REMOVER ===
tr(f'{B}/custom/card_remover.txt', [
    ('mes "Good day, young one. I have the power to remove cards that you have compounded onto your equipment. Does this idea please you?";', 'mes "Bom dia, jovem. Eu tenho o poder de remover cartas que voce compos no seu equipamento. Essa ideia te agrada?";'),
    ('select("Yes, it does.:What do you charge?:No thanks.")', 'select("Sim, agrada.:Quanto voce cobra?:Nao, obrigado.")'),
    ('mes "Very well. Which item shall I examine for you?";', 'mes "Muito bem. Qual item devo examinar para voce?";'),
    ("mes \"Young one... Your not wearing anything there that I can remove cards from.\";", 'mes "Jovem... Voce nao esta usando nada ai de onde eu possa remover cartas.";'),
    ("mes \"Young one... There are no cards compounded on this item. I can do nothing with it, I'm afraid.\";", 'mes "Jovem... Nao ha cartas compostas neste item. Infelizmente nao posso fazer nada com ele.";'),
    ('mes "^3355FFJust a minute!";', 'mes "^3355FFEspere um momento!";'),
    ("mes \"I can't offer any of my\";", 'mes "Eu nao posso oferecer";'),
    ('mes "services to you because";', 'mes "nenhum dos meus servicos";'),
    ("mes \"you're carrying too much\";", 'mes "porque voce esta carregando";'),
    ('mes "stuff. Put your extra items in";', 'mes "coisas demais. Guarde seus";'),
    ('mes "Kafra Storage and come again~";', 'mes "itens extras no Armazem Kafra e volte~";'),
    ('mes "This item has " + .@cardcount + " cards compounded on it. To perform my magic, I will need " + (.zenycost+(.@cardcount * .percardcost)) + " zeny, a ^0000FFStar Crumb^000000, and a ^0000FFYellow Gemstone^000000.";', 'mes "Este item tem " + .@cardcount + " cartas compostas nele. Para realizar minha magia, vou precisar de " + (.zenycost+(.@cardcount * .percardcost)) + " zeny, um ^0000FFStar Crumb^000000, e uma ^0000FFYellow Gemstone^000000.";'),
    ('select("Very well. Do it.:Never mind.")', 'select("Muito bem. Faca isso.:Deixa pra la.")'),
    ('mes "Very well. Return at once if you seek my services.";', 'mes "Muito bem. Volte quando precisar dos meus servicos.";'),
    ('mes "You do not have all the items I require to work my magic, child. Come again when you do.";', 'mes "Voce nao tem todos os itens que preciso para fazer minha magia, crianca. Volte quando tiver.";'),
    ('mes "Before I begin, I must warn you--I may fail. If I do, I may destroy the cards, the item, or both. I do not give refunds. That being said, which is more important to you: The cards, or the item?";', 'mes "Antes de comecar, devo te avisar--eu posso falhar. Se isso acontecer, posso destruir as cartas, o item, ou ambos. Eu nao dou reembolso. Dito isso, o que e mais importante pra voce: As cartas, ou o item?";'),
    ('select("I changed my mind about this.:The item.:The cards.")', 'select("Mudei de ideia sobre isso.:O item.:As cartas.")'),
    ('mes "Very well. I shall begin.";', 'mes "Muito bem. Vou comecar.";'),
    ('mes "The process was a total failure. I am afraid the item and the cards were destroyed.";', 'mes "O processo foi uma falha total. Infelizmente o item e as cartas foram destruidos.";'),
    ('mes "While I have managed to remove the cards from the item, they were destroyed in the process. The item, however, is okay.";', 'mes "Embora eu tenha conseguido remover as cartas do item, elas foram destruidas no processo. O item, porem, esta bem.";'),
    ('mes "Most unfortunate. I succeeded at removing the cards, but the item itself was destroyed in the process.";', 'mes "Que infelicidade. Consegui remover as cartas, mas o item em si foi destruido no processo.";'),
    ('mes "I have failed to remove the cards. Luckily, however, both the item and the cards are still okay.";', 'mes "Eu falhei em remover as cartas. Por sorte, porem, tanto o item quanto as cartas ainda estao bem.";'),
    ('mes "The process was a success. Here are your cards and your item. Farewell.";', 'mes "O processo foi um sucesso. Aqui estao suas cartas e seu item. Ate mais.";'),
    ('mes "I charge a flat fee of "+callfunc("F_InsertComma",.zenycost)+" zeny, plus "+callfunc("F_InsertComma",.percardcost)+" zeny for each card I remove from the item. In addition, I need a star crumb and a yellow gemstone to work my magic.";', 'mes "Eu cobro uma taxa fixa de "+callfunc("F_InsertComma",.zenycost)+" zeny, mais "+callfunc("F_InsertComma",.percardcost)+" zeny por cada carta que eu remover do item. Alem disso, preciso de um star crumb e uma yellow gemstone para fazer minha magia.";'),
])

# === CARD SELLER ===
tr(f'{B}/custom/card_seller.txt', [
    ('mes "I am sorry, it seems like something went wrong.";', 'mes "Desculpe, parece que algo deu errado.";'),
    ('mes "I cannot find any cards in our database at the moment.";', 'mes "Nao consigo encontrar nenhuma carta no nosso banco de dados no momento.";'),
    ('mes "Please contact a game master.";', 'mes "Por favor, entre em contato com um game master.";'),
    ('mes "Welcome!";', 'mes "Bem-vindo!";'),
    ('mes "I can sell you any normal monster card in the game. Would you like to have a look?";', 'mes "Posso te vender qualquer carta de monstro normal do jogo. Gostaria de dar uma olhada?";'),
])

# === ITEM SIGNER ===
tr(f'{B}/custom/item_signer.txt', [
    ('mes "I can ^0055FFsign your name^000000 on almost any rare item you hold.";', 'mes "Eu posso ^0055FFassinar seu nome^000000 em quase qualquer item raro que voce tenha.";'),
    ('select("Tell me more...:Sign my items, please!")', 'select("Me conte mais...:Assine meus itens, por favor!")'),
    ('mes "I can put your name on any slotless equipment or weapon.";', 'mes "Eu posso colocar seu nome em qualquer equipamento ou arma sem slot.";'),
    ('mes "For my work I accept:";', 'mes "Pelo meu trabalho eu aceito:";'),
    ('mes "I work for free, but...";', 'mes "Eu trabalho de graca, mas...";'),
    ('mes "Alas, I have 12 hungry children";', 'mes "Infelizmente, tenho 12 filhos famintos";'),
    ('mes "and a very angry wife.";', 'mes "e uma esposa muito brava.";'),
    ('mes "Or it was 12 angry children";', 'mes "Ou eram 12 filhos bravos";'),
    ('mes "and a very hungry wife...";', 'mes "e uma esposa muito faminta...";'),
    ('mes "Show me your items to sign...";', 'mes "Me mostre seus itens para assinar...";'),
    ('mes "Nothing is equipped there!";', 'mes "Nao tem nada equipado ai!";'),
    ("mes \"Alas, this item's already signed.\";", 'mes "Infelizmente, este item ja esta assinado.";'),
    ("mes \"I would never touch a master's work.\";", 'mes "Eu nunca tocaria no trabalho de um mestre.";'),
    ('mes "A card? Here?!";', 'mes "Uma carta? Aqui?!";'),
    ("mes \"As I said before, I don't sign items with cards.\";", 'mes "Como eu disse antes, eu nao assino itens com cartas.";'),
    ("mes \"Sorry, I don't sign slotted items.\";", 'mes "Desculpe, eu nao assino itens com slot.";'),
    ("mes \"Sorry, I don't sign rental items!\";", 'mes "Desculpe, eu nao assino itens alugados!";'),
    ('mes "I will need:";', 'mes "Vou precisar de:";'),
    ('select("Ok!:Leave")', 'select("Ok!:Sair")'),
    ('mes "See you...";', 'mes "Ate mais...";'),
    ("mes \"I don't work for 'thanks'.\";", 'mes "Eu nao trabalho por \'obrigado\'.";'),
    ('mes "Done!";', 'mes "Pronto!";'),
])

# === PLATINUM SKILLS ===
tr(f'{B}/custom/platinum_skills.txt', [
    ('mes "I can give you the special skills available to your job.";', 'mes "Eu posso te dar as habilidades especiais disponiveis para sua classe.";'),
    ('mes "Would you like these skills now?";', 'mes "Gostaria dessas habilidades agora?";'),
    ('select("Yes Please:No")', 'select("Sim, por favor:Nao")'),
    ('mes "Have a nice day... >.>";', 'mes "Tenha um bom dia... >.>";'),
    ('mes "There you go!";', 'mes "Aqui esta!";'),
])

# === RESET NPC ===
tr(f'{B}/custom/resetnpc.txt', [
    ('mes "Sorry you can only reset "', 'mes "Desculpe, voce so pode resetar "'),
    ('" in your life."', '" na sua vida."'),
    ('mes "I am the Reset Girl.";', 'mes "Eu sou a Garota do Reset.";'),
    ('mes "You may only reset "', 'mes "Voce so pode resetar "'),
    ('mes "Please select the service you want:";', 'mes "Por favor, selecione o servico que deseja:";'),
    ('select("^FF3355Reset Skills:Reset Stats:Reset Both^000000:Cancel")', 'select("^FF3355Resetar Skills:Resetar Stats:Resetar Ambos^000000:Cancelar")'),
    ("mes \"Sorry, you don't have enough Zeny.\";", 'mes "Desculpe, voce nao tem Zeny suficiente.";'),
    ('mes "You can only reset "', 'mes "Voce so pode resetar "'),
    ('" in your life, are you sure?"', '" na sua vida, tem certeza?"'),
    ('select("Let me think:That\'s fine")', 'select("Deixa eu pensar:Tudo bem")'),
    ('mes "There you go!";', 'mes "Aqui esta!";'),
])

# === STYLIST ===
tr(f'{B}/custom/stylist.txt', [
    ('select(" ~ Cloth color: ~ Hairstyle: ~ Hair color")', 'select(" ~ Cor da roupa: ~ Estilo de cabelo: ~ Cor do cabelo")'),
    ('"This is style #"', '"Este e o estilo #"'),
    ('" ~ Next (^0055FF"', '" ~ Proximo (^0055FF"'),
    ('" ~ Previous (^0055FF"', '" ~ Anterior (^0055FF"'),
    ('" ~ Jump to..."', '" ~ Ir para..."'),
    ('" ~ Revert to original (^0055FF"', '" ~ Voltar ao original (^0055FF"'),
    ('"Choose a style between 1 - "', '"Escolha um estilo entre 1 - "'),
])

# === JOBMASTER ===
tr(f'{B}/custom/jobmaster.txt', [
    ('mes "Level requirement:";', 'mes "Requisito de nivel:";'),
    ('mes "You need " +', 'mes "Voce precisa de " +'),
    ('"^bb0000"+.@blvl+"^000000 more base levels "', '"^bb0000"+.@blvl+"^000000 niveis base a mais "'),
    ('"and " : "") : "") +', '"e " : "") : "") +'),
    ('"^00bb00"+.@jlvl+"^000000 more job levels "', '"^00bb00"+.@jlvl+"^000000 niveis de classe a mais "'),
    ('"to continue."', '"para continuar."'),
    ('mes "Please remove your " +', 'mes "Por favor, remova seu " +'),
    ('? "falcon" : "")', '? "falcao" : "")'),
    ('? "cart" : "")', '? "carrinho" : "")'),
    ('? "mount" : "")', '? "montaria" : "")'),
    ('" before proceeding."', '" antes de continuar."'),
    ('mes "Please use all your skill points before proceeding.";', 'mes "Por favor, use todos os seus pontos de habilidade antes de continuar.";'),
    ('mes "An error has occurred.";', 'mes "Ocorreu um erro.";'),
    ('mes "No more jobs are available.";', 'mes "Nao ha mais classes disponiveis.";'),
    ('mes "Select a job.";', 'mes "Selecione uma classe.";'),
    ('" ~ ^777777Cancel^000000"', '" ~ ^777777Cancelar^000000"'),
    ('mes "A base level of " + .SNovice +', 'mes "E necessario nivel base " + .SNovice +'),
    ('" is required to turn into a " + jobname(.@class) + ".";', '" para se tornar um " + jobname(.@class) + ".";'),
    ('mes "You are now " + callfunc("F_InsertArticle", jobname(.@to_cls)) + "!";', 'mes "Agora voce e um " + jobname(.@to_cls) + "!";'),
    ('mes "Unknown Class Error.";', 'mes "Erro de classe desconhecida.";'),
    ('mes "Do you want to change into ^0055FF"+jobname(.@class)+"^000000 class?";', 'mes "Voce quer mudar para a classe ^0055FF"+jobname(.@class)+"^000000?";'),
    ('.@job_option$ = " ~ Change into ^0055FF"+jobname(.@class)+"^000000 class";', '.@job_option$ = " ~ Mudar para ^0055FF"+jobname(.@class)+"^000000";'),
    ('?"Go back" : "Cancel"', '?"Voltar" : "Cancelar"'),
])

print("=== Core custom files re-translated ===")

# Clean up this script
os.remove('N:/Users/tinch/Documents/Projetos/ragnarok/apply_translations.py')
print("Done!")
