#!/usr/bin/env python3
"""Translate rAthena NPC files from English to Brazilian Portuguese.
Only translates text inside mes "..." and select("...").
Does NOT change: variable names, function calls, NPC names in [],
item names, map names, coordinates, script logic, comments.
Uses informal BR-PT WITHOUT accented chars.
"""
import re
import os
import sys

# ===== MASTER TRANSLATION TABLE =====
# Key = exact English text inside quotes
# Value = Portuguese translation
T = {}

# ===== BG_COMMON =====
T.update({
    "Wise adventurer, why don't you lend us your power for victory?":
        "Sabio aventureiro, por que nao nos empresta seu poder pela vitoria?",
    "What's the reason for the Battle?:Tell me about General Guillaume":
        "Qual o motivo da Batalha?:Me fale sobre o General Guillaume",
    "Maroll's great king, Marcel Marollo VII, is very sick lately.":
        "O grande rei de Maroll, Marcel Marollo VII, esta muito doente ultimamente.",
    "His Majesty has declared that he will be leaving the future of Maroll to me or the 3rd prince, General Guillaume.":
        "Sua Majestade declarou que deixara o futuro de Maroll para mim ou para o 3o principe, General Guillaume.",
    "General Guillaume may have an advantage in this battle as he is the great general of Maroll, but that doesn't automatically mean he'll win.":
        "O General Guillaume pode ter uma vantagem nesta batalha por ser o grande general de Maroll, mas isso nao significa que ele vencera.",
    "I want to win this battle so that I can bring prosperity to the people of Maroll. They've suffered enough from war...":
        "Quero vencer esta batalha para trazer prosperidade ao povo de Maroll. Eles ja sofreram demais com a guerra...",
    "Yes, I want to join you.:End Conversation":
        "Sim, quero me juntar a voce.:Encerrar Conversa",
    "Thank you so much. I feel like I can win with the help of adventurers like you.":
        "Muito obrigado. Sinto que posso vencer com a ajuda de aventureiros como voce.",
    "Now, please go downstairs and join your comrades in sharpening their skills to fight the enemy!":
        "Agora, por favor desca e junte-se aos seus camaradas para aprimorar suas habilidades contra o inimigo!",
    "For Maroll!": "Por Maroll!",
    "The 3rd Prince Guillaume is the great general of Maroll.":
        "O 3o Principe Guillaume e o grande general de Maroll.",
    "It's a waste of time to explain to you how great a leader or warlord he is, since he commands the great military power of Maroll.":
        "E perda de tempo explicar o quao grande lider ou guerreiro ele e, ja que comanda o grande poder militar de Maroll.",
    "Unfortunately, there's something he and his followers are unaware of:":
        "Infelizmente, ha algo que ele e seus seguidores desconhecem:",
    "Do the people of Maroll really want them to spend so much money on military power?":
        "O povo de Maroll realmente quer que gastem tanto dinheiro em poder militar?",
    "We have suffered enough from wars.": "Ja sofremos demais com as guerras.",
    "I believe weapons aren't the best way to bring prosperity to a nation.":
        "Acredito que armas nao sao a melhor forma de trazer prosperidade a uma nacao.",
    "I do not wish to shed blood, but I have no choice but to fight for the possibility of peace and for the sake of my people.":
        "Nao desejo derramar sangue, mas nao tenho escolha senao lutar pela possibilidade de paz e pelo bem do meu povo.",
    "What's the reason for the Battle?:Tell me about Prince Croix":
        "Qual o motivo da Batalha?:Me fale sobre o Principe Croix",
    "Hot-blooded adventurer, we need your ability to win this battle.":
        "Aventureiro destemido, precisamos de sua habilidade para vencer esta batalha.",
    "Our great king, Marcel Marollo VII, is very sick lately.":
        "Nosso grande rei, Marcel Marollo VII, esta muito doente ultimamente.",
    "His Majesty has declared that he has chosen either me or Prince Croix as the next king amongst his 9 sons.":
        "Sua Majestade declarou que escolheu eu ou o Principe Croix como proximo rei entre seus 9 filhos.",
    "Two kings can't share a nation! Only the one victorious from His Majesty's appointed battle will be enthroned.":
        "Dois reis nao podem dividir uma nacao! Apenas o vitorioso da batalha designada por Sua Majestade sera entronizado.",
    "This is, however, not just a battle between us. This battle will determine the future of this country.":
        "Isso, no entanto, nao e apenas uma batalha entre nos. Esta batalha determinara o futuro deste pais.",
    "I pledge on my honor to prove that I'm the one who can protect this Maroll from outside threats.":
        "Juro pela minha honra provar que sou eu quem pode proteger Maroll de ameacas externas.",
    "Welcome to my army, comrade.": "Bem-vindo ao meu exercito, camarada.",
    "Your eyes tell me that you're a soldier that I can trust.":
        "Seus olhos me dizem que voce e um soldado em quem posso confiar.",
    "Now, go upstairs and apply for battle with your comrades.":
        "Agora, suba e se inscreva para a batalha com seus camaradas.",
    "I'm sure they'll welcome you whole-heartedly!":
        "Tenho certeza que te receberao de coracao aberto!",
    "I'll be the one who will capture the flag!":
        "Serei eu quem capturara a bandeira!",
    "The 5th Prince Croix is currently titled as the Prime Minister of Maroll.":
        "O 5o Principe Croix atualmente tem o titulo de Primeiro Ministro de Maroll.",
    "He thinks all national matters of a nation can be discussed and determined on a desk,":
        "Ele acha que todos os assuntos nacionais podem ser discutidos e decididos em uma mesa,",
    "and believes in peaceful co-existence with other countries.":
        "e acredita na coexistencia pacifica com outros paises.",
    "He's too ignorant to admit that so-called peace is built on countless lives that are sacrificed in wars while normal citizens and upper classes can live, oblivious to the horrors that allow them to live that way.":
        "Ele e ignorante demais para admitir que a chamada paz e construida sobre inumeras vidas sacrificadas em guerras enquanto cidadaos comuns e classes altas vivem alheios aos horrores que permitem viver assim.",
    "He's too naive to understand the reality....":
        "Ele e ingenuo demais para entender a realidade....",
    "I can't leave Maroll to someone like him who lives in a dream!":
        "Nao posso deixar Maroll para alguem como ele que vive em um sonho!",
    "His unrealistic beliefs will drown this country in poverty and make the people weak. If he becomes the king, Maroll will never rest from the onslaughts of other countries.":
        "Suas crencas irrealistas afogarao este pais na pobreza e enfraqucerao o povo. Se ele se tornar rei, Maroll nunca descansara dos ataques de outros paises.",
    "I want to teach him what makes this small country so powerful and prosperous. It's military power!":
        "Quero ensina-lo o que torna este pequeno pais tao poderoso e prospero. E o poder militar!",
    "I want to join your army!:End Conversation":
        "Quero me juntar ao seu exercito!:Encerrar Conversa",
    "Now, go upstairs and apply for battle from your comrades.":
        "Agora, suba e se inscreva para a batalha com seus camaradas.",
    "Do you wish to leave the battlefield? Use my services to return to town.":
        "Deseja sair do campo de batalha? Use meus servicos para voltar a cidade.",
    "Leave:Don't Leave": "Sair:Nao Sair",
    "I'll be here whenever you're in need of my services.":
        "Estarei aqui sempre que precisar dos meus servicos.",
    "Good day, adventurer.": "Bom dia, aventureiro.",
    "I'm a knight from a far country called Maroll Kingdom.":
        "Sou um cavaleiro de um pais distante chamado Reino de Maroll.",
    "The two princes of the kingdom are now battling for the throne of Maroll, and are in need of experienced soldiers like you.":
        "Os dois principes do reino estao lutando pelo trono de Maroll e precisam de soldados experientes como voce.",
    "How would you like to lend your power to one of the princes in the Maroll Kingdom?":
        "Gostaria de emprestar seu poder a um dos principes do Reino de Maroll?",
    "Join:Don't Join": "Entrar:Nao Entrar",
    "May the war god bless you.": "Que o deus da guerra te abencoe.",
    "I'll always be stationed here for more soldiers. Feel free to come back whenever you're interested.":
        "Estarei sempre estacionado aqui para mais soldados. Sinta-se livre para voltar quando tiver interesse.",
    "- Wait a minute !! -": "- Espere um minuto !! -",
    "- Currently you're carrying -": "- Atualmente voce esta carregando -",
    "- too many items with you. -": "- muitos itens com voce. -",
    "- Please try again -": "- Por favor tente novamente -",
    "- after you lose some weight. -": "- depois de perder um pouco de peso. -",
    "Do you have the battlefield badges?": "Voce tem as insignias do campo de batalha?",
    "I can exchange Bravery Badges and Valor Badges for reward items.":
        "Posso trocar Insignias de Bravura e Insignias de Valor por itens de recompensa.",
    "Exchange Badges:Check the Catalog": "Trocar Insignias:Ver o Catalogo",
    "Which type of items would you like to exchange?":
        "Que tipo de itens voce gostaria de trocar?",
    "To check more information about the reward items, please use our ^3131FFCatalog^000000.":
        "Para mais informacoes sobre os itens de recompensa, por favor use nosso ^3131FFCatalogo^000000.",
    "Weapon:Armor:Accessory:Consumable": "Arma:Armadura:Acessorio:Consumivel",
    "You chose ^3131FFWeapon^000000.": "Voce escolheu ^3131FFArma^000000.",
    "The following weapons are available for exchange with the battlefield badges.":
        "As seguintes armas estao disponiveis para troca com as insignias do campo de batalha.",
    "Please note that items for ^3131FFBravery Badges are indicated as (BB)^000000, and ^3131FFValor Badges as (VB)^000000.":
        "Note que itens de ^3131FFInsignias de Bravura sao indicados como (BB)^000000, e ^3131FFInsignias de Valor como (VB)^000000.",
    "The following items are available in the ^3131FFDagger, One-Handed Sword, Two-Handed Sword, and Two-Handed Spear^000000 category.":
        "Os seguintes itens estao disponiveis na categoria ^3131FFAdaga, Espada de Uma Mao, Espada de Duas Maos e Lanca de Duas Maos^000000.",
    "The following items are available in the ^3131FFStaff / Mace / Two-Handed Axe / Huuma Shuriken^000000 category.":
        "Os seguintes itens estao disponiveis na categoria ^3131FFCajado / Maca / Machado de Duas Maos / Huuma Shuriken^000000.",
    "The following weapons are available in the ^3131FFBow / Katar / Musical Instrument / Whip^000000 category.":
        "As seguintes armas estao disponiveis na categoria ^3131FFArco / Katar / Instrumento Musical / Chicote^000000.",
    "The following weapons are available in the ^3131FFBook / Knuckle^000000 category.":
        "As seguintes armas estao disponiveis na categoria ^3131FFLivro / Soqueira^000000.",
    "The following weapons are available in the ^3131FFRevolver / Rifle / Gatling Gun / Shotgun / Grenade Launcher^000000 category.":
        "As seguintes armas estao disponiveis na categoria ^3131FFRevolver / Rifle / Metralhadora Gatling / Escopeta / Lancador de Granadas^000000.",
    "Do not exchange:Exchange": "Nao trocar:Trocar",
    "Would you like to exchange?": "Gostaria de trocar?",
    "Yes:No": "Sim:Nao",
    "Remember, Battleground Reward Items are ^FF0000Character Bound^000000. Are you sure you want this item?":
        "Lembre-se, Itens de Recompensa do Campo de Batalha sao ^FF0000vinculados ao personagem^000000. Tem certeza que quer este item?",
    "Thank you for exchanging.": "Obrigado pela troca.",
    "I'm sorry, but you don't have enough badges to exchange.":
        "Desculpe, mas voce nao tem insignias suficientes para trocar.",
    "Do you need more time to check the items?": "Precisa de mais tempo para verificar os itens?",
    "You chose ^3131FFArmor^000000.": "Voce escolheu ^3131FFArmadura^000000.",
    "The following armors are available for exchange with the battlefield badges.":
        "As seguintes armaduras estao disponiveis para troca com as insignias do campo de batalha.",
    "Garments / Shoes:Armor": "Vestimentas / Calcados:Armadura",
    "You chose ^3131FFAccessory^000000.": "Voce escolheu ^3131FFAcessorio^000000.",
    "You can exchange the Medal of Honors with your Badges according to the job classes, as follows:":
        "Voce pode trocar as Medalhas de Honra com suas Insignias de acordo com as classes:",
    "You chose ^3131FFConsumable^000000.": "Voce escolheu ^3131FFConsumivel^000000.",
    "The following consumable items are available for exchange with the battlefield badges:":
        "Os seguintes itens consumiveis estao disponiveis para troca com as insignias do campo de batalha:",
    "We have many items, so please take a look and purchase deliberately.":
        "Temos muitos itens, entao por favor de uma olhada e compre com cuidado.",
    "This item is for Swordman and Taekwon Master Class only.": "Este item e apenas para classes Espadachim e Mestre Taekwon.",
    "This item is for Thief Class only.": "Este item e apenas para classe Gatuno.",
    "This item is for Acolyte Class only.": "Este item e apenas para classe Acolito.",
    "This item is for Magician Class only.": "Este item e apenas para classe Mago.",
    "This item is for Archer Class only.": "Este item e apenas para classe Arqueiro.",
    "This item is for Merchant Class only.": "Este item e apenas para classe Mercador.",
    "This item is for Gunslinger only.": "Este item e apenas para Pistoleiro.",
    "Which Badge do you want to exchange?": "Qual Insignia voce quer trocar?",
    "You cancelled the exchange.": "Voce cancelou a troca.",
    "Bravery Badge:Valor Badge:Cancel": "Insignia de Bravura:Insignia de Valor:Cancelar",
    "Blessed Guillaume!": "Guillaume abencoado!",
    "Blessed Croix!": "Croix abencoado!",
    "Let's enjoy our glorious victory!": "Vamos aproveitar nossa gloriosa vitoria!",
    "You lost, but you're dedicated to this battle.": "Voce perdeu, mas foi dedicado a esta batalha.",
    "This is a reward for your great dedication by Guillaume Marollo!":
        "Esta e uma recompensa pela sua grande dedicacao por Guillaume Marollo!",
    "Just take this defeat as a lesson, and next time you will definitely win.":
        "Apenas tome esta derrota como licao, e na proxima vez voce com certeza vencera.",
    "Even though we didn't win, we did our best.":
        "Mesmo que nao tenhamos vencido, demos o nosso melhor.",
    "This is a Royal gift from Croix, and please don't forget this battle. We will win the next one.":
        "Este e um presente Real de Croix, por favor nao esqueca esta batalha. Venceremos a proxima.",
    "The command has been cancelled.": "O comando foi cancelado.",
    "May I help you?": "Posso ajuda-lo?",
    "Close Battlefield:Open Battlefield:Reset a01:Reset b01:Reset a02:Reset b02":
        "Fechar Campo de Batalha:Abrir Campo de Batalha:Resetar a01:Resetar b01:Resetar a02:Resetar b02",
    "Complete": "Completo",
})

# ===== COOL EVENT CORP =====
T.update({
    "Welcome to Cool Event Corp.": "Bem-vindo a Cool Event Corp.",
    "Our staff is always working": "Nossa equipe esta sempre trabalhando",
    "to surpass your expactations": "para superar suas expectativas",
    "for quality service. So how": "de servico de qualidade. Entao como",
    "may I assist you today?": "posso ajuda-lo hoje?",
    "Your Respawn Point": "Seu Ponto de Retorno",
    "has been saved here": "foi salvo aqui",
    "Thank you for using the": "Obrigado por usar o",
    "Cool Event Corp. service~": "servico da Cool Event Corp.~",
    "I'm sorry, but you": "Desculpe, mas voce",
    "need the Novice's": "precisa da habilidade",
    "Basic Skill Level 6 to": "Basica de Novato nivel 6 para",
    "use the Storage Service.": "usar o Servico de Armazem.",
    "I'm sorry, but you don't": "Desculpe, mas voce nao",
    "have enough Zeny to use": "tem Zeny suficiente para usar",
    "the Storage Service. Our": "o Servico de Armazem. Nossa",
    "Storage access fee is 40 Zeny.": "taxa de acesso ao Armazem e de 40 Zeny.",
    "Let me open your personal": "Deixe-me abrir seu",
    "storage for you right away.": "armazem pessoal agora mesmo.",
    "Thanks for supporting Cool": "Obrigado por apoiar a Cool",
    "Event Corp. by using our": "Event Corp. usando nossos",
    "services. Have a good day~": "servicos. Tenha um bom dia~",
    "Please choose": "Por favor escolha",
    "your destination.": "seu destino.",
    "I'm sorry, but you don't have": "Desculpe, mas voce nao tem",
    "enough zeny for the Teleport": "zeny suficiente para o Servico",
    "Service. The fee to teleport": "de Teleporte. A taxa para teleportar",
    "I'm sorry, but the": "Desculpe, mas o",
    "Pushcart rental service": "servico de aluguel de Carrinho",
    "is only available to Merchant classes.": "esta disponivel apenas para classes Mercador.",
    "is only available to Merchants,": "esta disponivel apenas para Mercadores,",
    "Blacksmiths, White Smiths,": "Ferreiros, Mestre Ferreiros,",
    "Alchemists and Creators.": "Alquimistas e Criadores.",
    "You can only rent a cart after": "Voce so pode alugar um carrinho apos",
    "learning the Pushcart Skill.": "aprender a habilidade Carrinho.",
    "You already have": "Voce ja tem",
    "a Pushcart equipped.": "um Carrinho equipado.",
    "Unfortunately, we can't": "Infelizmente, nao podemos",
    "rent more than one to": "alugar mais de um para",
    "each customer at a time.": "cada cliente por vez.",
    "The Pushcart rental": "O aluguel de Carrinho",
    "fee is 800 Zeny. Would": "e de 800 Zeny. Gostaria de",
    "you like to rent a Pushcart?": "alugar um Carrinho?",
    "Rent a Pushcart:Cancel": "Alugar Carrinho:Cancelar",
    "don't have enough": "nao tem",
    "Zeny to pay the Pushcart": "Zeny suficiente para pagar o",
    "rental fee of 800 Zeny.": "aluguel de Carrinho de 800 Zeny.",
    "Cool Event Corp. is always": "A Cool Event Corp. esta sempre",
    "striving to provide the best": "se esforcando para oferecer os melhores",
    "services for our customers.": "servicos para nossos clientes.",
    "Help us become the best by": "Ajude-nos a ser os melhores",
    "providing us with your opinions": "nos dando suas opinioes",
    "and honest feedback. Thank you.": "e feedback sincero. Obrigado.",
    "Save:Use Storage::Rent a Pushcart:Storage Password Service:Cancel":
        "Salvar:Usar Armazem::Alugar Carrinho:Servico de Senha do Armazem:Cancelar",
    "Save:Use Storage:Teleport Service:Rent a Pushcart:Storage Password Service:Cancel":
        "Salvar:Usar Armazem:Servico de Teleporte:Alugar Carrinho:Servico de Senha do Armazem:Cancelar",
})

# ===== KAFRA FUNCTIONS =====
T.update({
    "Welcome to the": "Bem-vindo a",
    "Kafra Corporation.": "Corporacao Kafra.",
    "The Kafra services": "Os servicos Kafra",
    "are always on your side.": "estao sempre ao seu lado.",
    "How may I assist you?": "Como posso ajuda-lo?",
    "^666666W-weeeelc-c-come": "^666666B-beem-v-vindo",
    "to th-the K-kaaafrrrra": "a-a C-coorpoor-r-racao",
    "C-coorpoor-r-ratioooonn...^000000": "K-kaaafrrrra...^000000",
    "The Kafra Coporation will stay with you wherever you go.":
        "A Corporacao Kafra ficara com voce onde quer que va.",
    "So, have you come from a faraway land to study our culture, or are you just sightseeing?":
        "Entao, voce veio de uma terra distante para estudar nossa cultura, ou esta apenas passeando?",
    "In either case, why not stay awhile?": "Em qualquer caso, por que nao fica um pouco?",
    "The air is eternally heavy with the": "O ar e eternamente carregado com o",
    "scent of pleasant wildflowers.": "perfume de agradaveis flores silvestres.",
    "With our many Kafra": "Com nossas muitas",
    "service locations, you're never": "localizacoes de servico Kafra, voce nunca",
    "far from home.": "esta longe de casa.",

    # Menu arrays - these are in setarray calls, we handle via string replacement
    # Storage function
    "I'm sorry but another guild member is using the guild storage":
        "Desculpe, mas outro membro da guilda esta usando o armazem da guilda",
    "right now.  Please wait until that person is finished.":
        "agora. Por favor, espere ate que essa pessoa termine.",
    "I'm sorry, but you": "Desculpe, mas voce",
    "need the Novice's": "precisa da habilidade",
    "Basic Skill Level 6 to": "Basica de Novato nivel 6 para",
    "use the Storage Service.": "usar o Servico de Armazem.",
    "^666666S-s-ssoooorry,": "^666666D-d-deeesculllpe,",
    "y-you're a-a-aaaa": "v-voce e-e u-u-um",
    "Nooviiice... N-neeeds": "Noovaaato... P-precisa",
    "B-basic sssskill l-level 6...^000000": "H-habilidade b-basica n-nivel 6...^000000",
    "have enough zeny to use": "tem zeny suficiente para usar",
    "the Storage Service. Our": "o Servico de Armazem. Nossa",
    "^666666Zeeeeeny...": "^666666Zeeeeeny...",
    "M-more z-zeny...!": "M-mais z-zeny...!",
    "N-neeed 150... zeny...": "P-preciso de 150... zeny...",
    "Ergh! T-taking bl-blood~!": "Ergh! T-tirando s-sangue~!",
    "Here, let me open": "Aqui, deixe-me abrir",
    "your Storage for you.": "seu Armazem para voce.",
    "Thank you for using": "Obrigado por usar",
    "the Kafra Service.": "o Servico Kafra.",
    "^666666Thank you.. for... using...^000000": "^666666Obrigado.. por... usar...^000000",

    # Teleport
    "your destination.": "seu destino.",

    # Cart
    "Pushcart rental service": "servico de aluguel de Carrinho",
    "is only available to Merchant classes.": "esta disponivel apenas para classes Mercador.",
    "is only available to Merchants,": "esta disponivel apenas para Mercadores,",
    "Blacksmiths, Master Smiths,": "Ferreiros, Mestre Ferreiros,",
    "Alchemists and Biochemists.": "Alquimistas e Bioquimicos.",
    "a Pushcart equipped.": "um Carrinho equipado.",
    "rent more than one to": "alugar mais de um para",
    "each customer at a time.": "cada cliente por vez.",
    'You can only rent a cart after learning the "Push Cart" skill.':
        'Voce so pode alugar um carrinho apos aprender a habilidade "Push Cart".',
    "Rent a Pushcart.:Cancel": "Alugar Carrinho.:Cancelar",
    "zeny to pay the Pushcart": "zeny suficiente para pagar o aluguel",

    # Info
    "Check Special Reserve Points.": "Verificar Pontos de Reserva Especial.",
    "Storage Password Service": "Servico de Senha do Armazem",
    "Kafra Employee Locations": "Localizacao das Funcionarias Kafra",
    "Cancel": "Cancelar",
    "Let's see...": "Deixe-me ver...",
    "Ah, you have a total of": "Ah, voce tem um total de",
    "Special Reserve Points.": "Pontos de Reserva Especial.",
    "You can exchange your": "Voce pode trocar seus",
    "Special Reserve Points for": "Pontos de Reserva Especial por",
    "rewards at the Kafra Main Office in Al De Baran. Please use our":
        "recompensas na Sede Kafra em Al De Baran. Por favor use nossos",
    "convenient services to see the benefits of our rewards program.":
        "servicos convenientes para ver os beneficios do nosso programa de recompensas.",

    # End function
    "has been saved here": "foi salvo aqui",
    "Thank you for using": "Obrigado por usar",
    "the Kafra Services.": "os Servicos Kafra.",
    "We, here at Kafra Corporation,": "Nos, da Corporacao Kafra,",
    "are always endeavoring to provide you with the best services. We hope that we meet your adventuring needs and standards of excellence.":
        "estamos sempre nos esforcando para oferecer os melhores servicos. Esperamos atender suas necessidades de aventura e padroes de excelencia.",
    "^666666Kaffffra n-never": "^666666Kaffffra n-nunca",
    "diiiiiiiiiiiiiies. On...": "mooooooorre. No...",
    "On y-yooour siiiiide~^000000": "S-seu laaaaaado~^000000",
    "Saved.": "Salvo.",
    "Thank you for your patronage.": "Obrigado pela sua preferencia.",

    # Password functions
    "Enter your storage password:": "Digite sua senha do armazem:",
    "Wrong storage password.": "Senha do armazem incorreta.",
    "Additional storage protection with a password.":
        "Protecao adicional do armazem com uma senha.",
    "Your storage is protected with a password. What would you do now?":
        "Seu armazem esta protegido com uma senha. O que gostaria de fazer agora?",
    "At first, please enter your ^0000FFold password^000000.":
        "Primeiro, por favor digite sua ^0000FFsenha antiga^000000.",
    "Wrong password. You can't set a new password.":
        "Senha incorreta. Voce nao pode definir uma nova senha.",
    "Please, enter your password before its removal.":
        "Por favor, digite sua senha antes da remocao.",
    "The password hasn't been removed.": "A senha nao foi removida.",
    "You don't have enough zeny.": "Voce nao tem zeny suficiente.",
    "You've successfully cleared your storage password.":
        "Voce limpou sua senha do armazem com sucesso.",
    "Wrong password. We won't return your 1000z.":
        "Senha incorreta. Nao devolveremos seus 1000z.",
    "Please, next time enter correct password.":
        "Por favor, da proxima vez digite a senha correta.",
    "Now enter your ^FF0000new password^000000 to protect your storage from thieves.":
        "Agora digite sua ^FF0000nova senha^000000 para proteger seu armazem de ladroes.",
    "The password hasn't been changed.": "A senha nao foi alterada.",
    "You've protected your storage with a secret password.":
        "Voce protegeu seu armazem com uma senha secreta.",
    "Enter a number 1000~10000000:": "Digite um numero de 1000~10000000:",
    "You can't use such big password.": "Voce nao pode usar uma senha tao grande.",
    "You shouldn't use such short password.": "Voce nao deveria usar uma senha tao curta.",

    # Einbroch specific
    "Because of the ^FF0000Limited": "Por causa do ^FF0000Acordo de",
    "Transport Agreement^000000, the": "Transporte Limitado^000000, a",
    "Kafra Corporation cannot": "Corporacao Kafra nao pode",
    "provide Teleport Services": "fornecer Servicos de Teleporte",
    "in the Schwarzwald Republic.": "na Republica de Schwarzwald.",
    "We ask that you please": "Pedimos que por favor",
    "use the Airship Service": "use o Servico de Aeronave",
    "instead. Thank you for your": "em vez disso. Obrigado pela sua",
    "understanding and cooperation.": "compreensao e cooperacao.",
})

# ===== KAFRAS.TXT - City kafra dialogues =====
T.update({
    "Hm...?": "Hm...?",
    "Oh, welcome to": "Ah, bem-vindo a",
    "the Kafra Corporation": "Corporacao Kafra",
    "Headquarters. Did you": "Sede. Voce",
    "need something?": "precisa de algo?",
    "Save:Use Storage:Rent a Pushcart:Cancel":
        "Salvar:Usar Armazem:Alugar Carrinho:Cancelar",
    "Your Respawn Point has": "Seu Ponto de Retorno foi",
    "been saved here, inside": "salvo aqui, dentro",
    "of the Kafra Corporation": "da Sede da",
    "Headquarters. Thank you.": "Corporacao Kafra. Obrigado.",
    "Please make use of": "Por favor, faca uso dos",
    "the Kafra Services that are": "Servicos Kafra que estao",
    "available throughout all of": "disponiveis em todo",
    "Midgard. Thank you for": "Midgard. Obrigado por",
    "visiting the Kafra Headquarters.": "visitar a Sede da Kafra.",
    "Excuse me, but it": "Com licenca, mas",
    "seems that you don't": "parece que voce nao",
    "have the 20 zeny to pay": "tem os 20 zeny para pagar",
    "the Storage access fee...": "a taxa de acesso ao Armazem...",
    "Although this facility is": "Embora esta instalacao seja",
    "exclusively intended for": "exclusivamente destinada ao",
    "the training of Kafra Employee": "treinamento de Funcionarias Kafra",
    "and administrative functions,": "e funcoes administrativas,",
    "I'll access your Storage for you.": "vou acessar seu Armazem para voce.",
    "In the future, please": "No futuro, por favor",
    "ask the Kafra Employee on": "peca a Funcionaria Kafra de",
    "duty if you wish to use": "plantao se desejar usar",
    "any of the Kafra Services.": "qualquer um dos Servicos Kafra.",
    "Thank you for your patronage.": "Obrigado pela sua preferencia.",
    "My apologies, but I'm": "Desculpas, mas",
    "not on duty. I'd assist you": "nao estou de plantao. Eu ajudaria",
    "if I could, but actually don't": "se pudesse, mas na verdade nao",
    "have any available Pushcarts.": "tenho Carrinhos disponiveis.",
    "Why don't you ask another Kafra": "Por que nao pede a outra",
    "Employee for assistance?": "Funcionaria Kafra?",
    "Kafra Employees are": "Funcionarias Kafra estao",
    "stationed all over the": "posicionadas por todo o",
    "Midgard continent,": "continente de Midgard,",
    "and you should be able to find": "e voce deve conseguir encontrar",
    "plenty outside in Al De Baran.": "varias do lado de fora em Al De Baran.",
    "^666666*Whew...*^000000": "^666666*Ufa...*^000000",
    "Great, because I'm": "Otimo, porque estou",
    "actually on my break": "na verdade em meu intervalo",
    "right now. Choosing": "agora. Escolher",
    "''Cancel'' was a good": "''Cancelar'' foi uma boa",
    "move on your part.": "escolha da sua parte.",

    # Common kafra greetings
    "The Kafra Corporation": "A Corporacao Kafra",
    "is always working to provide": "esta sempre trabalhando para oferecer",
    "you with convenient services.": "servicos convenientes a voce.",
    "How may I be of assistance?": "Como posso ser util?",
    "Welcome~!": "Bem-vindo~!",
    "The Kafra Services": "Os Servicos Kafra",
    "So how can I help you?": "Entao como posso ajuda-lo?",
    "Welcome!": "Bem-vindo!",
    "will always support the": "sempre apoiara os",
    "adventurers of Rune-Midgarts": "aventureiros de Rune-Midgarts",
    "with its excellent service. So": "com seu excelente servico. Entao",
    "what can I do for you today?": "o que posso fazer por voce hoje?",
    "Welcome to the": "Bem-vindo a",
    "Kafra Corporation~": "Corporacao Kafra~",
    "The Kafra Services are": "Os Servicos Kafra estao",
    "always here to support": "sempre aqui para apoiar",
    "you. So how can I be": "voce. Entao como posso ser",
    "of service today?": "util hoje?",
    "Kafra's Employees are": "As Funcionarias da Kafra estao",
    "always ready to serve you.": "sempre prontas para servi-lo.",
    "How can I help you today?": "Como posso ajuda-lo hoje?",
    "You know that our": "Voce sabe que nosso",
    "service is always": "servico esta sempre",
    "on your side~": "ao seu lado~",

    # Location saves
    "in the city of Al De Baran": "na cidade de Al De Baran",
    "in the city of Geffen": "na cidade de Geffen",
    "in the city of Morocc": "na cidade de Morocc",
    "in the city of Payon": "na cidade de Payon",
    "in the city of Prontera": "na cidade de Prontera",
    "in the city of Juno": "na cidade de Juno",
    "in the city of Alberta": "na cidade de Alberta",
    "in the town of Comodo": "na cidade de Comodo",
    "in Pyros Lighthouse": "no Farol de Pyros",
    "in the city of Izlude": "na cidade de Izlude",
    "in the city of Moscovia": "na cidade de Moscovia",
    "in the city of Amatsu": "na cidade de Amatsu",
    "in the city of Ayothaya": "na cidade de Ayothaya",
    "in the town of Einbech": "na cidade de Einbech",
    "in the city of Einbroch": "na cidade de Einbroch",
    "in the city of Kunlun": "na cidade de Kunlun",
    "in the city of Lighthalzen": "na cidade de Lighthalzen",
    "in the city of Luoyang": "na cidade de Luoyang",
    "in the city of Umbala": "na cidade de Umbala",
    "in the city of Niflheim": "na cidade de Niflheim",
    "in the city of Brasilis": "na cidade de Brasilis",
    "at Byalan Island": "na Ilha Byalan",
    "at the Prontera Culverts": "nos Esgotos de Prontera",
    "at Mjolnir Dead Pit": "no Poco Morto de Mjolnir",
    "at the Pyramids": "nas Piramides",
    "at the Orc Dungeon": "na Masmorra dos Orcs",
    "at Sunken Ship": "no Navio Naufragado",
    "in the town of Rachel": "na cidade de Rachel",
    "in the town of Veins": "na cidade de Veins",
    "in the village of Hugel": "na vila de Hugel",
    "in the city of Dewata": "na cidade de Dewata",
    "at the Turbo Track Arena": "na Arena Turbo Track",
})

# ===== DTS WARPER =====
T.update({
    "Greetings, adventurer.": "Saudacoes, aventureiro.",
    "As you may be aware, we": "Como voce deve saber, nos",
    "are holding an election to": "estamos realizando uma eleicao para",
    "determine which company will": "determinar qual empresa ira",
    "provide the Dungeon Teleport": "fornecer o Servico de Teleporte",
    "Service. How may I help you?": "de Masmorra. Como posso ajuda-lo?",
    "Reason for Election:Cast a Vote:Use Teleport Service:Cancel":
        "Motivo da Eleicao:Votar:Usar Servico de Teleporte:Cancelar",
    "Cool Event Corp and the": "A Cool Event Corp e a",
    "Kafra Corporation have both": "Corporacao Kafra ambas",
    "been planning to provide a": "estavam planejando fornecer um",
    "Teleport Service to dungeons.": "Servico de Teleporte para masmorras.",
    "But due to technological": "Mas devido a limitacoes",
    "limitations, only one company": "tecnologicas, apenas uma empresa",
    "can serve as provider for this": "pode servir como provedora deste",
    "Dungeon Teleport Service at a": "Servico de Teleporte de Masmorra por",
    "time. There, both companies have agreed to hold special elections.":
        "vez. Assim, ambas as empresas concordaram em realizar eleicoes especiais.",
    "Each company has its own": "Cada empresa tem suas proprias",
    "policies and guarantees in": "politicas e garantias em",
    "regards to the Dungeon Teleport Service, and in this election, the":
        "relacao ao Servico de Teleporte de Masmorra, e nesta eleicao, os",
    "customers will ultimately decide and choose what's best for them.":
        "clientes irao decidir e escolher o que e melhor para eles.",
    "For now, the Dungeon": "Por enquanto, o Servico de",
    "Teleport Service will be": "Teleporte de Masmorra sera",
    "provided in a series of trial periods. This way, customers can":
        "fornecido em uma serie de periodos de teste. Desta forma, clientes podem",
    "see the benefits of both companies before making the final decision.":
        "ver os beneficios de ambas as empresas antes de tomar a decisao final.",
    "If you are qualified,": "Se voce esta qualificado,",
    "please vote in each election": "por favor vote em cada eleicao",
    "to decide which company will": "para decidir qual empresa ira",
    "Service for the next trial period. Thank you for your support~":
        "de Masmorra para o proximo periodo de teste. Obrigado pelo seu apoio~",
    "We, the Kafra Corporation,": "Nos, a Corporacao Kafra,",
    "are planning to provide the": "estamos planejando fornecer o",
    "Dungeon Teleport Service": "Servico de Teleporte de Masmorra",
    "to the following dungeons...": "para as seguintes masmorras...",
    "If you are interested in": "Se voce esta interessado em",
    "a Teleport Service to this": "um Servico de Teleporte para esta",
    "area, then please vote for": "area, entao por favor vote por",
    "us. Would you like to vote": "nos. Gostaria de votar",
    "for the Kafra Corporation?": "pela Corporacao Kafra?",
    "No:Yes": "Nao:Sim",
    "I understand. But if you": "Entendo. Mas se voce",
    "happen to change your mind,": "mudar de ideia,",
    "you are welcome to come back": "sera bem-vindo para voltar",
    "at any time. Thank you and": "a qualquer momento. Obrigado e",
    "have a good day, adventurer.": "tenha um bom dia, aventureiro.",
    "Thanks for your vote!": "Obrigado pelo seu voto!",
    "We'll continue to do our best": "Continuaremos fazendo o nosso melhor",
    "to provide the highest quality": "para fornecer o servico de",
    "service to our customers. Have": "mais alta qualidade aos nossos clientes. Tenha",
    "a good day and remember that the Kafra service is on your side~":
        "um bom dia e lembre-se que o servico Kafra esta sempre ao seu lado~",
    "I'm sorry, but you've ": "Desculpe, mas voce ja ",
    "I'm sorry, but you've": "Desculpe, mas voce ja",
    "already participated in": "participou desta",
    "this election. When the next": "eleicao. Quando a proxima",
    "election comes, you will be": "eleicao chegar, voce podera",
    "able to vote once again.": "votar novamente.",
    "Thank you for your support~": "Obrigado pelo seu apoio~",
    "After totalling the number of": "Apos totalizar o numero de",
    "votes from the last election,": "votos da ultima eleicao,",
    "we have concluded that the": "concluimos que a",
    "minimum voter participation": "condicao de participacao minima",
    "condition was not satisfied.": "de eleitores nao foi satisfeita.",
    "Therefore, another election to": "Portanto, outra eleicao para",
    "provide the Dungeon Teleport": "fornecer o Servico de Teleporte",
    "Service will be held. The Kafra": "de Masmorra sera realizada. A",
    "Corporation will teleport to": "Corporacao Kafra teleportara para",
    "the following dungeons...": "as seguintes masmorras...",
    "a Teleport Service to these": "um Servico de Teleporte para estas",
    "areas, then please vote for": "areas, entao por favor vote por",
    "for the Kafra Corporation?": "pela Corporacao Kafra?",
    "Service will be held. However,": "de Masmorra sera realizada. Porem,",
    "since you've already voted, you cannot vote again in this election.":
        "como voce ja votou, nao pode votar novamente nesta eleicao.",
    "Your participation in these": "Sua participacao nestas",
    "elections is much appreciated,": "eleicoes e muito apreciada,",
    "and we encourage you to vote": "e encorajamos voce a votar",
    "again during the next election.": "novamente na proxima eleicao.",
    "Thank you and have a nice day~": "Obrigado e tenha um bom dia~",
    "I'm sorry, but there are": "Desculpe, mas nao ha",
    "no elections taking place at": "eleicoes acontecendo no",
    "this time. When the polls are": "momento. Quando as votacoes",
    "open, we encourage you to take": "abrirem, encorajamos voce a",
    "part and voice your opinions.": "participar e dar sua opiniao.",
    "Thank you for choosing the": "Obrigado por escolher o",
    "Dungeon Teleport Service.": "Servico de Teleporte de Masmorra.",
    "Please keep in mind that the": "Por favor tenha em mente que os",
    "Free Warp Tickets and Kafra": "Tickets de Warp Gratis e os Pontos",
    "Special Reserve Points do not": "de Reserva Especial Kafra nao se",
    "apply in this special service.": "aplicam neste servico especial.",
    "have enough money to pay": "tem dinheiro suficiente para pagar",
    "the 4,000 zeny fee to teleport": "a taxa de 4.000 zeny para teleportar",
    "to the Toy Factory. Please": "para a Toy Factory. Por favor",
    "check your funds again.": "verifique seus fundos novamente.",
    "to the Clock Tower. Please": "para a Clock Tower. Por favor",
    "to the Lava Dungeon. Please": "para a Lava Dungeon. Por favor",
    "I'm sorry, but because of": "Desculpe, mas por causa dos",
    "the results from the most": "resultados da mais",
    "recent election, Cool Event": "recente eleicao, a Cool Event",
    "Corp. is currently handling": "Corp. esta atualmente cuidando do",
    "the Dungeon Teleport Service. We apologize for the inconvenience.":
        "Servico de Teleporte de Masmorra. Pedimos desculpas pelo inconveniente.",
    "is not active during the voting": "nao esta ativo durante o periodo",
    "period. Once the election is": "de votacao. Quando a eleicao",
    "over, the Dungeon Teleport": "terminar, o Servico de Teleporte",
    "Service will become available.": "de Masmorra ficara disponivel.",
    "We, here at Kafra Corporation,": "Nos, da Corporacao Kafra,",
    "are always endeavoring to provide you with the best services. We hope that we meet your adventuring needs and standards of excellence.":
        "estamos sempre nos esforcando para oferecer os melhores servicos. Esperamos atender suas necessidades de aventura e padroes de excelencia.",

    # Cool Event Corp Voting Staff
    "Hello! Don't forget to make": "Ola! Nao esqueca de fazer",
    "your voice be heard and make": "sua voz ser ouvida e",
    "sure you vote in the elections": "certifique-se de votar nas eleicoes",
    "between Cool Event Corp. and": "entre a Cool Event Corp. e a",
    "Kafra Corporation for control of the Dungeon Teleport Service!":
        "Corporacao Kafra pelo controle do Servico de Teleporte de Masmorra!",
    "Cool Event Corp. has been": "A Cool Event Corp. estava",
    "planning to provide a new": "planejando fornecer um novo",
    "Dungeon Teleport Service to": "Servico de Teleporte de Masmorra para",
    "its customers, a service not": "seus clientes, um servico nao",
    "already provided by the Kafra": "ja fornecido pela",
    "Corporation. However...": "Corporacao Kafra. Porem...",
    "Kafra Corporation, which": "A Corporacao Kafra, que",
    "already monopolizes the": "ja monopoliza o",
    "public teleportation market,": "mercado publico de teleporte,",
    "actually also had plans to": "na verdade tambem tinha planos para",
    "provide a similar service.": "fornecer um servico similar.",
    "Because of technological": "Devido a limitacoes",
    "can be chosen as the provider": "pode ser escolhida como provedora",
    "of this Dungeon Teleport Service. Hence, we will let the customers":
        "deste Servico de Teleporte de Masmorra. Portanto, deixaremos os clientes",
    "decide through these elections.": "decidirem atraves destas eleicoes.",
    "Multiple elections will be": "Multiplas eleicoes serao",
    "held so that our customers": "realizadas para que nossos clientes",
    "can test out the special services of each company for themselves.":
        "possam testar os servicos especiais de cada empresa por si mesmos.",
    "However, keep in mind that you must be eligible in order to vote.":
        "Porem, tenha em mente que voce precisa ser elegivel para votar.",
    "For voter eligibility": "Para informacoes sobre",
    "details, please visit our": "elegibilidade de voto, visite nossa",
    "headquarters in the city of": "sede na cidade de",
    "Lighthalzen located in the": "Lighthalzen localizada na",
    "Schwarzwald Republic.": "Republica de Schwarzwald.",
    "Thank you for your time.": "Obrigado pelo seu tempo.",
    "Cool Event Corp.,": "Cool Event Corp.,",
    "if chosen to provide the": "se escolhida para fornecer o",
    "Dungeon Teleport Service,": "Servico de Teleporte de Masmorra,",
    "will teleport adventurers to": "teleportara aventureiros para",
    "the following dungeons...": "as seguintes masmorras...",
    "these destinations, then": "estes destinos, entao",
    "it would be in your best": "seria do seu melhor",
    "interest to vote for us.": "interesse votar por nos.",
    "Would you like to vote": "Gostaria de votar",
    "for Cool Event Corp.?": "pela Cool Event Corp.?",
    "Ah, I see... Well, if you": "Ah, entendo... Bom, se voce",
    "feel free to come back and": "sinta-se livre para voltar e",
    "cast your vote for Cool Event": "dar seu voto para a Cool Event",
    "Corp, alright? Have a nice day~": "Corp, certo? Tenha um bom dia~",
    "Thank you for your vote!": "Obrigado pelo seu voto!",
    "It's customers like you who": "Sao clientes como voce que",
    "ensure the success and great": "garantem o sucesso e otimo",
    "service that you have come to": "servico que voce espera da",
    "expect from Cool Event Corp.": "Cool Event Corp.",
    "Thank you and have a nice day~": "Obrigado e tenha um bom dia~",
    "already cast your vote": "ja deu seu voto",
    "in this election. However,": "nesta eleicao. Porem,",
    "please don't let that stop you": "por favor nao deixe isso impedi-lo",
    "from voting for Cool Event": "de votar pela Cool Event",
    "Corp. in the next election~": "Corp. na proxima eleicao~",
    "Unfortunately, there wasn't": "Infelizmente, nao houve",
    "enough voter turnout in the": "participacao suficiente de eleitores na",
    "last election, so we're holding": "ultima eleicao, entao estamos realizando",
    "another election to determine": "outra eleicao para determinar",
    "which company will provide the": "qual empresa ira fornecer o",
    "We appreciate that": "Agradecemos que",
    "you've already participated": "voce ja participou",
    "in this second election by": "desta segunda eleicao",
    "casting your vote. Thank": "dando seu voto. Obrigado",
    "you for your support~": "pelo seu apoio~",
    "I'm sorry, but an election is": "Desculpe, mas uma eleicao nao",
    "not currently being held at this time. Please come and cast your":
        "esta sendo realizada no momento. Por favor venha e de seu",
    "vote at the next election to decide which company will provide the":
        "voto na proxima eleicao para decidir qual empresa ira fornecer o",
    "Please remember that we": "Por favor lembre-se que",
    "cannot accept Free Warp Tickets": "nao aceitamos Tickets de Warp Gratis",
    "or award Special Reserve Points": "ou concedemos Pontos de Reserva Especial",
    "for this service. Now, please": "para este servico. Agora, por favor",
    "choose your destination.": "escolha seu destino.",
    "I'm sorry, but you do": "Desculpe, mas voce nao",
    "not have enough zeny to": "tem zeny suficiente para",
    "teleport to this destination.": "teleportar para este destino.",
    "The teleport fee is 4,000 zeny.": "A taxa de teleporte e de 4.000 zeny.",
    "Always be assured that": "Tenha sempre a certeza de que a",
    "Cool Event Corp. will do": "Cool Event Corp. fara",
    "everything in its power to": "tudo ao seu alcance para",
    "ensure the satisfaction of": "garantir a satisfacao de",
    "its customers, young and old": "seus clientes, jovens e idosos",
    "and big and small. Thank you~": "grandes e pequenos. Obrigado~",
    "I'm sorry, but Cool Event": "Desculpe, mas a Cool Event",
    "Corp. does not currently offer": "Corp. nao oferece atualmente o",
    "the Dungeon Teleport Service": "Servico de Teleporte de Masmorra",
    "due to the results of the last": "devido aos resultados da ultima",
    "election. Please vote for us": "eleicao. Por favor vote por nos",
    "next time, alright? Good day~": "da proxima vez, certo? Bom dia~",
    "Dungeon Teleport Service is": "Servico de Teleporte de Masmorra esta",
    "unavailable during elections": "indisponivel durante as eleicoes",
    "and will be reactivated after the election results are announced.":
        "e sera reativado apos os resultados da eleicao serem anunciados.",
    "Thank you and have a nice day.": "Obrigado e tenha um bom dia.",
    "Cool Event Corp. is always": "A Cool Event Corp. esta sempre",
    "working to make sure that": "trabalhando para garantir que",
    "not only are our customers": "nao apenas nossos clientes estejam",
    "satisfied, but that we also": "satisfeitos, mas que tambem",
    "exceed your utmost standards.": "superemos seus mais altos padroes.",
    "Thank you and have a good day.": "Obrigado e tenha um bom dia.",

    # GM NPC (inside /* */ comment block but still translate)
    "Lady Christy!": "Lady Christy!",
    "I am Lady Christy's Maid.": "Eu sou a empregada de Lady Christy.",
    "Globalvar Check:Setitem Zero:Change Glbalvar":
        "Verificar Globalvar:Zerar Setitem:Alterar Globalvar",
    "Current GlobalVar are": "As GlobalVar atuais sao",
    "Which Globalvar value would you like to change?":
        "Qual valor de Globalvar voce gostaria de alterar?",
    "Please enter a number among 0 and 1000.": "Por favor digite um numero entre 0 e 1000.",
    "Please enter a number among 0 and 10000.": "Por favor digite um numero entre 0 e 10000.",
    "Please enter a number among 0 and 2.": "Por favor digite um numero entre 0 e 2.",
    "Please enter a number among 0 and 3.": "Por favor digite um numero entre 0 e 3.",
    "The value is incorrect.": "O valor esta incorreto.",
    "The value has been modified.": "O valor foi modificado.",
    "Lady Christy...": "Lady Christy...",
})


# ===== DYNAMIC STRING REPLACEMENTS =====
# These handle lines with string concatenation that can't be matched as single mes strings
DYNAMIC = [
    # bg_common.txt
    ('"You will be sent back to "', '"Voce sera enviado de volta para "'),
    ('strcharinfo(0)+", it\'s a sign reflecting victory."', 'strcharinfo(0)+", e um sinal que reflete a vitoria."'),
    ('"Oh, "+strcharinfo(0)+" Don\'t be sad."', '"Oh, "+strcharinfo(0)+" Nao fique triste."'),
    ('"You do not have enough "+getitemname(.@cost)+"s."', '"Voce nao tem "+getitemname(.@cost)+" suficientes."'),
    # functions_kafras.txt - setarray menu items
    ('"Use Storage"', '"Usar Armazem"'),
    ('"Use Guild Storage"', '"Usar Armazem da Guilda"'),
    ('"Rent a Pushcart"', '"Alugar Carrinho"'),
    ('"Use Teleport Service"', '"Usar Servico de Teleporte"'),
    ('"Cancel"', '"Cancelar"'),
    ('"Save"', '"Salvar"'),
    ('"Check Other Information"', '"Verificar Outras Informacoes"'),
    # functions_kafras.txt - dynamic fee messages
    ('"Storage access fee is " + .@fee + " zeny."', '"taxa de acesso ao Armazem e de " + .@fee + " zeny."'),
    ('"I\'m sorry, but you don\'t have"', '"Desculpe, mas voce nao tem"'),
    ('"enough zeny for the Teleport"', '"zeny suficiente para o Servico"'),
    ('"Service. The fee to teleport"', '"de Teleporte. A taxa para teleportar"'),
    ('"to " + @wrpD$[.@j] + " is " + @wrpP[.@j] + " zeny."', '"para " + @wrpD$[.@j] + " e de " + @wrpP[.@j] + " zeny."'),
    ('"fee is " + .@rental_fee + " zeny. Would"', '"e de " + .@rental_fee + " zeny. Gostaria de"'),
    ('"you like to rent a Pushcart?"', '"alugar um Carrinho?"'),
    ('"rental fee of " + .@rental_fee + " zeny."', '"aluguel de Carrinho de " + .@rental_fee + " zeny."'),
    # setarray menu items for password
    ('"Set new password -> 5000z"', '"Definir nova senha -> 5000z"'),
    ('"Change old password -> 5000z"', '"Alterar senha antiga -> 5000z"'),
    ('"Remove storage password -> 1000z"', '"Remover senha do armazem -> 1000z"'),
    # proudly presents (dynamic NPC name)
    ('" proudly presents you a new service:"', '" orgulhosamente apresenta um novo servico:"'),
    ('"to "+ .@destination$ +" is "+.@cost+" zeny."', '"para "+ .@destination$ +" e de "+.@cost+" zeny."'),
    # Guild member
    ('"Welcome. ^ff0000"', '"Bem-vindo. ^ff0000"'),
    ('"^000000 Member."', '"^000000 Membro."'),
    # strcharinfo
    ('"" + strcharinfo(0) + "..."', '"" + strcharinfo(0) + "..."'),
    ('"" + RESRVPTS + " Special Reserve Points."', '"" + RESRVPTS + " Pontos de Reserva Especial."'),
    ('"Thank you for using " + .@comp_name$ + "."', '"Obrigado por usar " + .@comp_name$ + "."'),
]


def translate_file(filepath):
    """Read file, translate mes/select content, write back."""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # Check skip condition
    if 'Cancelar' in content or 'voce' in content:
        print(f"SKIP (already translated): {os.path.basename(filepath)}")
        return 0

    original = content
    count = 0

    # First apply dynamic replacements (these handle string concatenation)
    for eng, ptbr in DYNAMIC:
        if eng in content:
            content = content.replace(eng, ptbr)
            count += content.count(ptbr)

    # Then translate mes "..." and select("...") lines
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith('//'):
            new_lines.append(line)
            continue

        orig_line = line

        # Handle mes "..."
        if 'mes "' in line:
            def repl_mes(m):
                nonlocal count
                txt = m.group(2)
                if txt.startswith('[') and txt.endswith(']'):
                    return m.group(0)
                if not txt.strip():
                    return m.group(0)
                if txt in T:
                    count += 1
                    return m.group(1) + T[txt] + m.group(3)
                return m.group(0)
            line = re.sub(r'(mes ")(.*?)(")', repl_mes, line)

        # Handle select("...")
        if 'select(' in line:
            def repl_sel(m):
                nonlocal count
                txt = m.group(2)
                if txt in T:
                    count += 1
                    return m.group(1) + T[txt] + m.group(3)
                return m.group(0)
            line = re.sub(r'(select\(")(.*?)("\))', repl_sel, line)

        new_lines.append(line)

    result = '\n'.join(new_lines)

    if result != original:
        with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
            f.write(result)
        print(f"TRANSLATED: {os.path.basename(filepath)} ({count} replacements)")
        return count
    else:
        print(f"NO CHANGES: {os.path.basename(filepath)}")
        return 0


if __name__ == '__main__':
    total = 0
    for fp in sys.argv[1:]:
        if os.path.isfile(fp):
            total += translate_file(fp)
    print(f"\nTotal replacements: {total}")
