"""
MyLogoQR - Comprehensive International Multi-Language SEO Engine
Languages: Spanish (/es/), Portuguese (/pt/), Russian (/ru/), Italian (/it/)
Generates 96 fully localized, client-side, indexable landing pages with hreflang tags,
sitemap update, .htaccess rewrite rules, and builds deployment archive.
"""

import os
import re
import json

WEBSITE_DIR = r"D:\Projects\mylogoqr\website"
HTACCESS_PATH = os.path.join(WEBSITE_DIR, ".htaccess")
SITEMAP_PATH = os.path.join(WEBSITE_DIR, "sitemap.xml")

LANGUAGES = {
    "es": {
        "name": "Español",
        "lang_code": "es",
        "locale": "es_ES",
        "og_locale": "es_ES",
        "header_gen": "Generadores",
        "header_use": "Cómo Usar",
        "header_blog": "Blog",
        "header_faq": "Preguntas",
        "header_about": "Acerca de",
        "header_contact": "Contacto",
        "header_cta": "Crear QR",
        "chips": ["Funciona en tu navegador", "Nunca caduca", "Escaneos ilimitados", "PNG y SVG"],
        "footer_desc": "El generador de códigos QR con logo líder, 100% en el navegador. Diseña códigos vectoriales de alta resolución con estilo de marca y máxima privacidad sin límites ni registro.",
        "footer_copy": "© 2026 MyLogoQR — Generador de Códigos QR Gratis y Privado. Todos los derechos reservados.",
        "footer_col_gen": "Generadores",
        "footer_col_res": "Recursos",
        "footer_col_legal": "Confianza y Legal",
        "footer_hub": "Directorio de Generadores",
        "footer_guides": "Guías y Blog",
        "footer_about": "Acerca de Nosotros",
        "footer_contact": "Soporte y Contacto",
        "footer_privacy": "Política de Privacidad",
        "footer_terms": "Términos de Servicio",
        "footer_cookie": "Política de Cookies",
        "footer_disclaimer": "Descargo de Responsabilidad",
        "lang_strip_title": "🌍 Versiones Internacionales:",
        "ui_your_content": "1. Tu contenido",
        "ui_quick_styles": "2. Estilos rápidos",
        "ui_colors": "3. Colores",
        "ui_dots_color": "Color de puntos",
        "ui_bg_color": "Color de fondo",
        "ui_logo": "4. Logotipo",
        "ui_upload_logo": "Subir logotipo",
        "ui_logo_size": "Tamaño del logo",
        "ui_download_png": "Descargar PNG",
        "ui_download_svg": "Descargar SVG",
        "ui_copy_link": "Copiar Enlace",
        "home_title": "Generador de Códigos QR con Logo Gratis — Personalizado y Vectorial | MyLogoQR",
        "home_desc": "Crea códigos QR personalizados con logo, colores de marca y degradados gratis. 100% privado en tu navegador, sin límites de escaneo ni vencimiento. Descarga PNG y SVG.",
        "home_h1": "Códigos QR que reflejan tu marca",
        "home_sub": "Agrega tu logotipo, personaliza los colores y descarga en segundos. Gratis, privado y sin registro.",
        "hub_title": "Directorio de Herramientas de Códigos QR Especializadas | MyLogoQR",
        "hub_desc": "Explora 22 generadores de códigos QR especializados y gratuitos con logotipo: WhatsApp, Wi-Fi, Instagram, vCard, Menús y más.",
        "hub_h1": "Todos los tipos de códigos QR especializados",
        "hub_sub": "Elige tu caso de uso específico para generar un código QR personalizado, vectorizado y con tu logo corporativo en segundos.",
        "guide_title": "Guía Práctica de Uso y Buenas Prácticas",
        "guide_tips_title": "Consejos Profesionales de Escaneo"
    },
    "pt": {
        "name": "Português",
        "lang_code": "pt",
        "locale": "pt_BR",
        "og_locale": "pt_BR",
        "header_gen": "Geradores",
        "header_use": "Como Usar",
        "header_blog": "Blog",
        "header_faq": "Perguntas",
        "header_about": "Sobre Nós",
        "header_contact": "Contato",
        "header_cta": "Criar QR",
        "chips": ["Roda no seu navegador", "Nunca expira", "Leituras ilimitadas", "PNG e SVG"],
        "footer_desc": "O principal gerador de QR Code gratuito com logotipo, 100% no navegador. Crie códigos de barras vetoriais de alta resolução com design de marca e privacidade total sem limites.",
        "footer_copy": "© 2026 MyLogoQR — Gerador de QR Code Grátis e Privado. Todos os direitos reservados.",
        "footer_col_gen": "Geradores",
        "footer_col_res": "Recursos",
        "footer_col_legal": "Confiança e Legal",
        "footer_hub": "Diretório de Geradores",
        "footer_guides": "Guias e Blog",
        "footer_about": "Sobre Nós",
        "footer_contact": "Suporte e Contato",
        "footer_privacy": "Política de Privacidade",
        "footer_terms": "Termos de Serviço",
        "footer_cookie": "Política de Cookies",
        "footer_disclaimer": "Isenção de Responsabilidade",
        "lang_strip_title": "🌍 Versões Internacionais:",
        "ui_your_content": "1. Seu conteúdo",
        "ui_quick_styles": "2. Estilos rápidos",
        "ui_colors": "3. Cores",
        "ui_dots_color": "Cor dos pontos",
        "ui_bg_color": "Cor de fundo",
        "ui_logo": "4. Logotipo",
        "ui_upload_logo": "Enviar logotipo",
        "ui_logo_size": "Tamanho do logo",
        "ui_download_png": "Baixar PNG",
        "ui_download_svg": "Baixar SVG",
        "ui_copy_link": "Copiar Link",
        "home_title": "Criar QR Code com Logo Grátis — Gerador de Código QR Personalizado | MyLogoQR",
        "home_desc": "Crie QR codes personalizados com logotipo, cores da sua marca e gradientes grátis. 100% privado no navegador, sem limite de leitura e sem expiração. Baixar PNG e SVG.",
        "home_h1": "Códigos QR com a identidade da sua marca",
        "home_sub": "Adicione seu logo, escolha as cores e baixe em segundos. Grátis, privado e sem cadastro.",
        "hub_title": "Diretório de Ferramentas de QR Code Especializadas | MyLogoQR",
        "hub_desc": "Explore 22 geradores de QR Code especializados e gratuitos com logotipo: WhatsApp, Wi-Fi, Instagram, vCard, Cardápios e mais.",
        "hub_h1": "Todos os tipos de códigos QR especializados",
        "hub_sub": "Escolha o tipo perfeito para criar um QR Code personalizado, vetorial e com seu logotipo corporativo em segundos.",
        "guide_title": "Guia Prático e Melhores Práticas",
        "guide_tips_title": "Dicas Profissionais de Leitura"
    },
    "ru": {
        "name": "Русский",
        "lang_code": "ru",
        "locale": "ru_RU",
        "og_locale": "ru_RU",
        "header_gen": "Генераторы",
        "header_use": "Инструкция",
        "header_blog": "Блог",
        "header_faq": "Вопросы",
        "header_about": "О нас",
        "header_contact": "Контакты",
        "header_cta": "Создать QR",
        "chips": ["Работает в браузере", "Без срока действия", "Безлимитные сканы", "PNG и SVG"],
        "footer_desc": "Ведущий бесплатный генератор QR-кодов с логотипом, работающий прямо в браузере. Векторные штрихкоды высокого разрешения без ограничений сканирования и без рекламы.",
        "footer_copy": "© 2026 MyLogoQR — Бесплатный и безопасный генератор QR-кодов. Все права защищены.",
        "footer_col_gen": "Генераторы",
        "footer_col_res": "Ресурсы",
        "footer_col_legal": "Безопасность",
        "footer_hub": "Каталог генераторов",
        "footer_guides": "Руководства и блог",
        "footer_about": "О проекте",
        "footer_contact": "Служба поддержки",
        "footer_privacy": "Политика конфиденциальности",
        "footer_terms": "Условия использования",
        "footer_cookie": "Политика cookie",
        "footer_disclaimer": "Отказ от ответственности",
        "lang_strip_title": "🌍 Международные версии:",
        "ui_your_content": "1. Ваша информация",
        "ui_quick_styles": "2. Быстрые стили",
        "ui_colors": "3. Цвета",
        "ui_dots_color": "Цвет точек",
        "ui_bg_color": "Цвет фона",
        "ui_logo": "4. Логотип",
        "ui_upload_logo": "Загрузить логотип",
        "ui_logo_size": "Размер логотипа",
        "ui_download_png": "Скачать PNG",
        "ui_download_svg": "Скачать SVG",
        "ui_copy_link": "Скопировать ссылку",
        "home_title": "Генератор QR кодов с логотипом бесплатно — Создать красивый QR код | MyLogoQR",
        "home_desc": "Создавайте персональные QR коды с логотипом, градиентом и фирменными цветами бесплатно. 100% приватно в браузере, без срока действия и без ограничений. Скачать PNG и SVG.",
        "home_h1": "QR коды в стиле вашего бренда",
        "home_sub": "Добавьте свой логотип, выберите цвета и скачайте за секунды. Бесплатно, безопасно и без регистрации.",
        "hub_title": "Каталог специализированных генераторов QR-кодов | MyLogoQR",
        "hub_desc": "22 специализированных бесплатных генератора QR-кодов с логотипом: WhatsApp, Wi-Fi, Instagram, визитки vCard, ресторанные меню и др.",
        "hub_h1": "Все виды специализированных QR-кодов",
        "hub_sub": "Выберите нужный тип и создайте персональный векторный QR-код с логотипом вашего бренда за считанные секунды.",
        "guide_title": "Практическое руководство и рекомендации",
        "guide_tips_title": "Профессиональные советы по сканированию"
    },
    "it": {
        "name": "Italiano",
        "lang_code": "it",
        "locale": "it_IT",
        "og_locale": "it_IT",
        "header_gen": "Generatori",
        "header_use": "Come Usare",
        "header_blog": "Blog",
        "header_faq": "Domande",
        "header_about": "Chi Siamo",
        "header_contact": "Contatti",
        "header_cta": "Crea QR",
        "chips": ["Funziona nel browser", "Nessuna scadenza", "Scansioni illimitate", "PNG e SVG"],
        "footer_desc": "Il principale generatore di codici QR gratuito con logo, 100% lato client. Crea codici a barre vettoriali ad alta risoluzione con stile aziendale e privacy totale.",
        "footer_copy": "© 2026 MyLogoQR — Generatore di Codici QR Gratuito e Privato. Tutti i diritti riservati.",
        "footer_col_gen": "Generatori",
        "footer_col_res": "Risorse",
        "footer_col_legal": "Note Legali",
        "footer_hub": "Directory Generatori",
        "footer_guides": "Guide e Blog",
        "footer_about": "Chi Siamo",
        "footer_contact": "Supporto e Contatti",
        "footer_privacy": "Informativa sulla Privacy",
        "footer_terms": "Termini di Servizio",
        "footer_cookie": "Informativa sui Cookie",
        "footer_disclaimer": "Disclaimer",
        "lang_strip_title": "🌍 Versioni Internazionali:",
        "ui_your_content": "1. Il tuo contenuto",
        "ui_quick_styles": "2. Stili rapidi",
        "ui_colors": "3. Colori",
        "ui_dots_color": "Colore dei punti",
        "ui_bg_color": "Colore di sfondo",
        "ui_logo": "4. Logo",
        "ui_upload_logo": "Carica logo",
        "ui_logo_size": "Dimensione logo",
        "ui_download_png": "Scarica PNG",
        "ui_download_svg": "Scarica SVG",
        "ui_copy_link": "Copia Link",
        "home_title": "Generatore Codice QR con Logo Gratis — Crea QR Code Personalizzato | MyLogoQR",
        "home_desc": "Crea codici QR personalizzati con logo, colori del tuo brand e gradienti gratis. 100% privato nel browser, senza limiti di scansione e senza scadenza. Scarica in PNG e SVG.",
        "home_h1": "Codici QR con l'identità del tuo brand",
        "home_sub": "Aggiungi il tuo logo, scegli i colori e scarica in pochi secondi. Gratuito, privato e senza registrazione.",
        "hub_title": "Directory Strumenti QR Code Specializzati | MyLogoQR",
        "hub_desc": "Esplora 22 generatori di codici QR gratuiti e specializzati con logo: WhatsApp, Wi-Fi, Instagram, vCard, Menu ristorante e altro.",
        "hub_h1": "Tutti i tipi di codici QR specializzati",
        "hub_sub": "Scegli il caso d'uso specifico per generare un codice QR personalizzato, vettoriale e con il logo del tuo brand in pochi secondi.",
        "guide_title": "Guida Pratica all'Uso e Best Practice",
        "guide_tips_title": "Consigli Professionali per la Scansione"
    }
}

# 22 Tools Metadata Translations
TOOL_META = {
    "whatsapp-qr-code-generator": {
        "es": {
            "title": "Generador de Códigos QR para WhatsApp con Logo Gratis | MyLogoQR",
            "desc": "Crea códigos QR personalizados para WhatsApp con tu logo. Inicia chats y mensajes directos al instante sin guardar números. Descarga PNG y SVG.",
            "h1": "Generador de Códigos QR para WhatsApp con Logo",
            "sub": "Permite que tus clientes te envíen mensajes de WhatsApp con un solo escaneo. Personaliza con tu logo y colores de marca.",
            "field": "Número de teléfono de WhatsApp (con código de país)",
            "msg_field": "Mensaje predeterminado (opcional)"
        },
        "pt": {
            "title": "Criar QR Code para WhatsApp com Logo Grátis | MyLogoQR",
            "desc": "Gere QR Codes personalizados para WhatsApp com o logo da sua empresa. Inicie conversas diretas sem precisar salvar o número. Baixar PNG e SVG.",
            "h1": "Gerador de QR Code para WhatsApp com Logotipo",
            "sub": "Facilite o contato de clientes abrindo uma conversa direta no WhatsApp ao escanear. Personalize com logotipo e cores.",
            "field": "Número de telefone do WhatsApp (com DDI e DDD)",
            "msg_field": "Mensagem pré-definida (opcional)"
        },
        "ru": {
            "title": "Генератор QR кодов WhatsApp с логотипом бесплатно | MyLogoQR",
            "desc": "Создайте красивый QR код для чата в WhatsApp с логотипом вашего бренда. Мгновенный переход в диалог без сохранения номера. Скачать PNG и SVG.",
            "h1": "Генератор QR кодов WhatsApp с логотипом",
            "sub": "Открывайте диалог в WhatsApp с вашим бизнесом в один клик. Добавьте логотип, градиенты и фирменные цвета.",
            "field": "Номер телефона WhatsApp (с кодом страны)",
            "msg_field": "Текст первого сообщения (необязательно)"
        },
        "it": {
            "title": "Generatore Codice QR WhatsApp con Logo Gratis | MyLogoQR",
            "desc": "Crea codici QR personalizzati per WhatsApp con il tuo logo. Avvia chat e messaggi diretti senza salvare il numero. Scarica in PNG e SVG vettoriale.",
            "h1": "Generatore Codice QR WhatsApp con Logo",
            "sub": "Permetti ai tuoi clienti di avviare una chat WhatsApp immediata con una semplice scansione. Personalizza con logo e colori del brand.",
            "field": "Numero di telefono WhatsApp (con prefisso internazionale)",
            "msg_field": "Messaggio predefinito (facoltativo)"
        }
    },
    "wifi-qr-code-generator": {
        "es": {
            "title": "Generador de Códigos QR para Wi-Fi con Contraseña y Logo | MyLogoQR",
            "desc": "Genera códigos QR de conexión rápida a Wi-Fi con tu logo. Comparte tu red sin revelar contraseñas complejas. 100% privado y seguro.",
            "h1": "Generador de Códigos QR para Wi-Fi con Logo",
            "sub": "Permite que invitados y clientes se conecten a tu Wi-Fi al instante con solo escanear la cámara de su teléfono.",
            "field": "Nombre de la red Wi-Fi (SSID)",
            "msg_field": "Contraseña de la red"
        },
        "pt": {
            "title": "Gerador de QR Code Wi-Fi com Senha e Logo Grátis | MyLogoQR",
            "desc": "Crie QR Codes de conexão Wi-Fi com logotipo para cafeterias, hotéis e escritórios. Conexão automática sem digitar senhas.",
            "h1": "Gerador de QR Code Wi-Fi com Logotipo",
            "sub": "Permita que clientes e hóspedes conectem à rede Wi-Fi escaneando com a câmera do celular. Seguro e prático.",
            "field": "Nome da rede Wi-Fi (SSID)",
            "msg_field": "Senha da rede Wi-Fi"
        },
        "ru": {
            "title": "Генератор QR кодов для Wi-Fi с паролем и логотипом | MyLogoQR",
            "desc": "Создайте QR код для быстрого подключения к Wi-Fi сети с логотипом заведения. Подключение в одно касание без ввода сложных паролей.",
            "h1": "Генератор QR кодов Wi-Fi с паролем и логотипом",
            "sub": "Гости и клиенты подключаются к вашему Wi-Fi мгновенно, просто наведя камеру телефона на стильный брендированный код.",
            "field": "Имя сети Wi-Fi (SSID)",
            "msg_field": "Пароль от Wi-Fi"
        },
        "it": {
            "title": "Generatore Codice QR Wi-Fi con Password e Logo | MyLogoQR",
            "desc": "Crea codici QR per connessione Wi-Fi rapida con il tuo logo. Condividi la tua rete in bar, uffici e hotel senza dettare la password.",
            "h1": "Generatore Codice QR Wi-Fi con Logo",
            "sub": "Consenti a ospiti e clienti di connettersi istantaneamente alla tua rete Wi-Fi inquadrando il codice con lo smartphone.",
            "field": "Nome della rete Wi-Fi (SSID)",
            "msg_field": "Password della rete Wi-Fi"
        }
    },
    "instagram-qr-code-generator": {
        "es": {
            "title": "Generador de Códigos QR para Instagram con Logo Gratis | MyLogoQR",
            "desc": "Crea códigos QR personalizados para tu perfil, reels o tienda de Instagram con logo. Vector SVG y PNG listos para imprimir.",
            "h1": "Generador de Códigos QR para Instagram con Logo",
            "sub": "Convierte el tráfico presencial en seguidores activos en Instagram. Abre directamente la app de Instagram al escanear.",
            "field": "URL de tu perfil o publicación de Instagram",
            "msg_field": ""
        },
        "pt": {
            "title": "Gerador de QR Code para Instagram com Logo Grátis | MyLogoQR",
            "desc": "Gere QR Codes personalizados para seu perfil, reels ou loja do Instagram com seu logo. Arquivos vetoriais em PNG e SVG.",
            "h1": "Gerador de QR Code para Instagram com Logo",
            "sub": "Transforme clientes físicos em seguidores fiéis no Instagram com um escaneamento rápido que abre o app direto.",
            "field": "Link do perfil ou publicação do Instagram",
            "msg_field": ""
        },
        "ru": {
            "title": "Генератор QR кодов для Instagram с логотипом | MyLogoQR",
            "desc": "Создайте красивый QR код со ссылкой на профиль Instagram с логотипом. Векторные файлы PNG и SVG для полиграфии и упаковки.",
            "h1": "Генератор QR кодов для Instagram с логотипом",
            "sub": "Привлекайте подписчиков в ваш аккаунт Instagram из офлайна с помощью брендированного сканируемого кода.",
            "field": "Ссылка на профиль или пост в Instagram",
            "msg_field": ""
        },
        "it": {
            "title": "Generatore Codice QR per Instagram con Logo Gratis | MyLogoQR",
            "desc": "Crea codici QR personalizzati per il tuo profilo o post Instagram con il tuo logo. File vettoriali PNG e SVG pronti per la stampa.",
            "h1": "Generatore Codice QR per Instagram con Logo",
            "sub": "Trasforma i visitatori in follower attivi su Instagram aprendo direttamente l'app con una rapida scansione.",
            "field": "Link al profilo o post di Instagram",
            "msg_field": ""
        }
    },
    "google-reviews-qr-code-generator": {
        "es": {
            "title": "Generador de Códigos QR para Reseñas de Google con Logo | MyLogoQR",
            "desc": "Multiplica tus reseñas de 5 estrellas en Google Maps. Códigos QR directos al formulario de valoración de tu negocio.",
            "h1": "Generador de Códigos QR para Reseñas de Google con Logo",
            "sub": "Lleva a tus clientes satisfechos directo a la pantalla de 5 estrellas en Google para disparar tu reputación local.",
            "field": "Enlace directo de reseñas de Google Business",
            "msg_field": ""
        },
        "pt": {
            "title": "Gerador de QR Code para Avaliações do Google com Logo | MyLogoQR",
            "desc": "Consiga mais avaliações de 5 estrelas no Google Meu Negócio com QR Codes diretos na tela de avaliação da sua empresa.",
            "h1": "Gerador de QR Code para Avaliações do Google com Logo",
            "sub": "Facilite o feedback dos seus clientes levando-os diretamente para a página de 5 estrelas no Google Maps.",
            "field": "Link de avaliação do Google Meu Negócio",
            "msg_field": ""
        },
        "ru": {
            "title": "Генератор QR кодов для отзывов в Google с логотипом | MyLogoQR",
            "desc": "Получайте больше положительных отзывов 5 звезд в Google Maps. QR код ведет прямо на форму оценки вашей компании.",
            "h1": "Генератор QR кодов для отзывов в Google",
            "sub": "Увеличьте рейтинг вашего бизнеса в Google, предоставив клиентам мгновенную ссылку на окно отзыва при сканировании.",
            "field": "Ссылка на форму отзыва в Google Business",
            "msg_field": ""
        },
        "it": {
            "title": "Generatore Codice QR per Recensioni Google con Logo | MyLogoQR",
            "desc": "Ottieni più recensioni a 5 stelle su Google Maps. Crea codici QR personalizzati che aprono direttamente la schermata recensione.",
            "h1": "Generatore Codice QR per Recensioni Google con Logo",
            "sub": "Migliora la tua reputazione locale portando i clienti soddisfatti direttamente alla pagina di recensione di Google.",
            "field": "Link diretto alla recensione Google Business",
            "msg_field": ""
        }
    },
    "restaurant-menu-qr-code-generator": {
        "es": {
            "title": "Generador de Códigos QR para Menú de Restaurante con Logo | MyLogoQR",
            "desc": "Crea códigos QR modernos para cartas y menús digitales en PDF o web. Resistentes al desgaste y con el logo de tu restaurante.",
            "h1": "Generador de Códigos QR para Menús y Cartas con Logo",
            "sub": "Permite que los comensales vean tu carta digital en sus propios teléfonos al sentarse a la mesa.",
            "field": "Enlace a tu menú digital o archivo PDF",
            "msg_field": ""
        },
        "pt": {
            "title": "Gerador de QR Code para Cardápio de Restaurante com Logo | MyLogoQR",
            "desc": "Crie QR Codes profissionais para cardápios digitais e menus em PDF com a identidade do seu restaurante ou bar.",
            "h1": "Gerador de QR Code para Cardápio de Restaurante com Logo",
            "sub": "Permita que seus clientes acessem o menu completo pelo celular assim que se sentarem à mesa.",
            "field": "Link do cardápio digital ou arquivo PDF",
            "msg_field": ""
        },
        "ru": {
            "title": "Генератор QR кодов для меню ресторана с логотипом | MyLogoQR",
            "desc": "Создайте удобный QR код для электронного меню ресторана или кафе с фирменным логотипом. Печать на тейбл-тентах и наклейках.",
            "h1": "Генератор QR кодов для ресторанного меню с логотипом",
            "sub": "Гости заведения мгновенно открывают онлайн-меню на смартфонах без необходимости листать бумажные буклеты.",
            "field": "Ссылка на онлайн-меню или PDF-файл",
            "msg_field": ""
        },
        "it": {
            "title": "Generatore Codice QR per Menu Ristorante con Logo | MyLogoQR",
            "desc": "Crea codici QR professionali per il menu digitale del tuo ristorante o bar. Vettoriali in alta risoluzione con il logo del tuo locale.",
            "h1": "Generatore Codice QR per Menu Ristorante con Logo",
            "sub": "Offri ai clienti un accesso immediato al menu digitale direttamente dal proprio smartphone al tavolo.",
            "field": "Link al menu digitale o al PDF online",
            "msg_field": ""
        }
    },
    "vcard-qr-code-generator": {
        "es": {
            "title": "Generador de Códigos QR vCard Tarjeta de Contacto con Logo | MyLogoQR",
            "desc": "Crea tarjetas de presentación digitales con QR vCard. Guarda teléfono, correo, empresa y redes en la agenda del teléfono con 1 toque.",
            "h1": "Generador de Códigos QR vCard con Logo",
            "sub": "Comparte todos tus datos de contacto profesionales al instante sin errores de escritura.",
            "field": "Nombre completo y datos de contacto",
            "msg_field": ""
        },
        "pt": {
            "title": "Gerador de QR Code vCard Cartão de Visitas Digital com Logo | MyLogoQR",
            "desc": "Gere cartões de visita digitais em QR Code. Salva nome, telefone, e-mail e cargo diretamente na agenda do smartphone.",
            "h1": "Gerador de QR Code vCard com Logotipo",
            "sub": "Faça networking inteligente compartilhando seu contato completo com uma simples leitura de câmera.",
            "field": "Nome completo e dados de contato",
            "msg_field": ""
        },
        "ru": {
            "title": "Генератор QR кодов vCard Электронная визитка с логотипом | MyLogoQR",
            "desc": "Создайте электронную визитку в формате QR-кода. Сохранение контакта, телефона, email и должности в телефонную книгу в один клик.",
            "h1": "Генератор QR кодов vCard с логотипом",
            "sub": "Делитесь контактами на конференциях и встречах: наведите камеру и контакт сразу сохраняется в смартфоне.",
            "field": "ФИО и контактные данные",
            "msg_field": ""
        },
        "it": {
            "title": "Generatore Codice QR vCard Biglietto da Visita con Logo | MyLogoQR",
            "desc": "Crea biglietti da visita digitali in formato vCard con logo. Salva telefono, email e azienda direttamente in rubrica.",
            "h1": "Generatore Codice QR vCard con Logo",
            "sub": "Scambia i tuoi contatti di lavoro in modo moderno e senza errori di battitura con un semplice tocco.",
            "field": "Nome e dettagli di contatto",
            "msg_field": ""
        }
    }
}

# Template for language switcher
def get_lang_switcher_header(current_lang="en", slug_path=""):
    clean_path = slug_path.lstrip("/")
    langs = [("en", "EN", ""), ("es", "ES", "es/"), ("pt", "PT", "pt/"), ("ru", "RU", "ru/"), ("it", "IT", "it/")]
    links = []
    for code, label, prefix in langs:
        href = f"/{prefix}{clean_path}".rstrip("/") if f"/{prefix}{clean_path}".rstrip("/") else "/"
        if clean_path and not href.endswith(clean_path):
            href = f"/{prefix}{clean_path}"
        active = ' class="active"' if code == current_lang else ''
        links.append(f'<a href="{href}"{active} title="{code.upper()}">{label}</a>')
    return f'<div class="lang-switch" style="display:inline-flex;gap:3px;background:#F1F5F9;padding:3px 6px;border-radius:8px;font-size:0.78rem;font-weight:700;margin-left:8px;align-items:center">{"".join(links)}</div>'

def get_lang_strip_footer(current_lang="en", slug_path=""):
    clean_path = slug_path.lstrip("/")
    langs = [
        ("en", "English", ""),
        ("es", "Español", "es/"),
        ("pt", "Português", "pt/"),
        ("ru", "Русский", "ru/"),
        ("it", "Italiano", "it/")
    ]
    links = []
    for code, label, prefix in langs:
        href = f"/{prefix}{clean_path}".rstrip("/") if f"/{prefix}{clean_path}".rstrip("/") else "/"
        if clean_path and not href.endswith(clean_path):
            href = f"/{prefix}{clean_path}"
        weight = 'font-weight:700;color:#FFFFFF' if code == current_lang else 'color:#94A3B8'
        links.append(f'<a href="{href}" style="display:inline;padding:0 6px;text-decoration:none;{weight}">{label}</a>')
    
    title = LANGUAGES.get(current_lang, {}).get("lang_strip_title", "🌍 International Versions:")
    return (
        f'<div class="lang-bar" style="margin-top:28px;padding-top:20px;border-top:1px solid rgba(255,255,255,0.08);text-align:center;font-size:0.86rem;color:#94A3B8">\n'
        f'  <span style="color:#CBD5E1;font-weight:600;margin-right:8px">{title}</span>\n'
        f'  {" &bull; ".join(links)}\n'
        f'</div>'
    )

def get_hreflang_tags(slug_path=""):
    clean_path = slug_path.lstrip("/")
    tags = [
        f'<link rel="alternate" hreflang="x-default" href="https://mylogoqr.com/{clean_path}" />',
        f'<link rel="alternate" hreflang="en" href="https://mylogoqr.com/{clean_path}" />',
        f'<link rel="alternate" hreflang="es" href="https://mylogoqr.com/es/{clean_path}" />',
        f'<link rel="alternate" hreflang="pt" href="https://mylogoqr.com/pt/{clean_path}" />',
        f'<link rel="alternate" hreflang="ru" href="https://mylogoqr.com/ru/{clean_path}" />',
        f'<link rel="alternate" hreflang="it" href="https://mylogoqr.com/it/{clean_path}" />'
    ]
    return "\n".join(tags)

print("Engine base functions and translation mappings loaded.")

# Dictionary of all 22 tools with English base names, icons, and multilingual titles/subtitles/placeholders
ALL_TOOLS = [
    {
        "slug": "whatsapp-qr-code-generator",
        "icon": "💬",
        "es": {"title": "Generador de Códigos QR para WhatsApp con Logo Gratis | MyLogoQR", "desc": "Crea códigos QR personalizados para WhatsApp con tu logo. Inicia chats y mensajes directos al instante sin guardar números. Descarga PNG y SVG.", "h1": "Generador de Códigos QR para WhatsApp con Logo", "sub": "Permite que tus clientes te envíen mensajes de WhatsApp con un solo escaneo. Personaliza con tu logo y colores de marca."},
        "pt": {"title": "Criar QR Code para WhatsApp com Logo Grátis | MyLogoQR", "desc": "Gere QR Codes personalizados para WhatsApp com o logo da sua empresa. Inicie conversas diretas sem precisar salvar o número. Baixar PNG e SVG.", "h1": "Gerador de QR Code para WhatsApp com Logotipo", "sub": "Facilite o contato de clientes abrindo uma conversa direta no WhatsApp ao escanear. Personalize com logotipo e cores."},
        "ru": {"title": "Генератор QR кодов WhatsApp с логотипом бесплатно | MyLogoQR", "desc": "Создайте красивый QR код для чата в WhatsApp с логотипом вашего бренда. Мгновенный переход в диалог без сохранения номера. Скачать PNG и SVG.", "h1": "Генератор QR кодов WhatsApp с логотипом", "sub": "Открывайте диалог в WhatsApp с вашим бизнесом в один клик. Добавьте логотип, градиенты и фирменные цвета."},
        "it": {"title": "Generatore Codice QR WhatsApp con Logo Gratis | MyLogoQR", "desc": "Crea codici QR personalizzati per WhatsApp con il tuo logo. Avvia chat e messaggi diretti senza salvare il numero. Scarica in PNG e SVG vettoriale.", "h1": "Generatore Codice QR WhatsApp con Logo", "sub": "Permetti ai tuoi clienti di avviare una chat WhatsApp immediata con una semplice scansione. Personalizza con logo e colori del brand."}
    },
    {
        "slug": "wifi-qr-code-generator",
        "icon": "📶",
        "es": {"title": "Generador de Códigos QR para Wi-Fi con Contraseña y Logo | MyLogoQR", "desc": "Genera códigos QR de conexión rápida a Wi-Fi con tu logo. Comparte tu red sin revelar contraseñas complejas. 100% privado y seguro.", "h1": "Generador de Códigos QR para Wi-Fi con Logo", "sub": "Permite que invitados y clientes se conecten a tu Wi-Fi al instante con solo escanear la cámara de su teléfono."},
        "pt": {"title": "Gerador de QR Code Wi-Fi com Senha e Logo Grátis | MyLogoQR", "desc": "Crie QR Codes de conexão Wi-Fi com logotipo para cafeterias, hotéis e escritórios. Conexão automática sem digitar senhas.", "h1": "Gerador de QR Code Wi-Fi com Logotipo", "sub": "Permita que clientes e hóspedes conectem à rede Wi-Fi escaneando com a câmera do celular. Seguro e prático."},
        "ru": {"title": "Генератор QR кодов для Wi-Fi с паролем и логотипом | MyLogoQR", "desc": "Создайте QR код для быстрого подключения к Wi-Fi сети с логотипом заведения. Подключение в одно касание без ввода сложных паролей.", "h1": "Генератор QR кодов Wi-Fi с паролем и логотипом", "sub": "Гости и клиенты подключаются к вашему Wi-Fi мгновенно, просто наведя камеру телефона на стильный брендированный код."},
        "it": {"title": "Generatore Codice QR Wi-Fi con Password e Logo | MyLogoQR", "desc": "Crea codici QR per connessione Wi-Fi rapida con il tuo logo. Condividi la tua rete in bar, uffici e hotel senza dettare la password.", "h1": "Generatore Codice QR Wi-Fi con Logo", "sub": "Consenti a ospiti e clienti di connettersi istantaneamente alla tua rete Wi-Fi inquadrando il codice con lo smartphone."}
    },
    {
        "slug": "instagram-qr-code-generator",
        "icon": "📸",
        "es": {"title": "Generador de Códigos QR para Instagram con Logo Gratis | MyLogoQR", "desc": "Crea códigos QR personalizados para tu perfil, reels o tienda de Instagram con logo. Vector SVG y PNG listos para imprimir.", "h1": "Generador de Códigos QR para Instagram con Logo", "sub": "Convierte el tráfico presencial en seguidores activos en Instagram. Abre directamente la app de Instagram al escanear."},
        "pt": {"title": "Gerador de QR Code para Instagram com Logo Grátis | MyLogoQR", "desc": "Gere QR Codes personalizados para seu perfil, reels ou loja do Instagram com seu logo. Arquivos vetoriais em PNG e SVG.", "h1": "Gerador de QR Code para Instagram com Logo", "sub": "Transforme clientes físicos em seguidores fiéis no Instagram com um escaneamento rápido que abre o app direto."},
        "ru": {"title": "Генератор QR кодов для Instagram с логотипом | MyLogoQR", "desc": "Создайте красивый QR код со ссылкой на профиль Instagram с логотипом. Векторные файлы PNG и SVG для полиграфии и упаковки.", "h1": "Генератор QR кодов для Instagram с логотипом", "sub": "Привлекайте подписчиков в ваш аккаунт Instagram из офлайна с помощью брендированного сканируемого кода."},
        "it": {"title": "Generatore Codice QR per Instagram con Logo Gratis | MyLogoQR", "desc": "Crea codici QR personalizzati per il tuo profilo o post Instagram con il tuo logo. File vettoriali PNG e SVG pronti per la stampa.", "h1": "Generatore Codice QR per Instagram con Logo", "sub": "Trasforma i visitatori in follower attivi su Instagram aprendo direttamente l'app con una rapida scansione."}
    },
    {
        "slug": "google-reviews-qr-code-generator",
        "icon": "⭐",
        "es": {"title": "Generador de Códigos QR para Reseñas de Google con Logo | MyLogoQR", "desc": "Multiplica tus reseñas de 5 estrellas en Google Maps. Códigos QR directos al formulario de valoración de tu negocio.", "h1": "Generador de Códigos QR para Reseñas de Google con Logo", "sub": "Lleva a tus clientes satisfechos directo a la pantalla de 5 estrellas en Google para disparar tu reputación local."},
        "pt": {"title": "Gerador de QR Code para Avaliações do Google com Logo | MyLogoQR", "desc": "Consiga mais avaliações de 5 estrelas no Google Meu Negócio com QR Codes diretos na tela de avaliação da sua empresa.", "h1": "Gerador de QR Code para Avaliações do Google com Logo", "sub": "Facilite o feedback dos seus clientes levando-os diretamente para a página de 5 estrelas no Google Maps."},
        "ru": {"title": "Генератор QR кодов для отзывов в Google с логотипом | MyLogoQR", "desc": "Получайте больше положительных отзывов 5 звезд в Google Maps. QR код ведет прямо на форму оценки вашей компании.", "h1": "Генератор QR кодов для отзывов в Google", "sub": "Увеличьте рейтинг вашего бизнеса в Google, предоставив клиентам мгновенную ссылку на окно отзыва при сканировании."},
        "it": {"title": "Generatore Codice QR per Recensioni Google con Logo | MyLogoQR", "desc": "Ottieni più recensioni a 5 stelle su Google Maps. Crea codici QR personalizzati che aprono direttamente la schermata recensione.", "h1": "Generatore Codice QR per Recensioni Google con Logo", "sub": "Migliora la tua reputazione locale portando i clienti soddisfatti direttamente alla pagina di recensione di Google."}
    },
    {
        "slug": "google-maps-qr-code-generator",
        "icon": "📍",
        "es": {"title": "Generador de Códigos QR para Google Maps con Logo | MyLogoQR", "desc": "Crea códigos QR de ubicación para tu negocio físico o evento. Abre navegación GPS directa en Google Maps y Waze.", "h1": "Generador de Códigos QR para Google Maps con Logo", "sub": "Guía a tus clientes directo a tu puerta con indicaciones de GPS inmediatas en Google Maps."},
        "pt": {"title": "Gerador de QR Code para Google Maps com Logo Grátis | MyLogoQR", "desc": "Crie QR Codes de localização para seu comércio ou evento. Abre o GPS diretamente no Google Maps e Waze.", "h1": "Gerador de QR Code para Google Maps com Logo", "sub": "Ajude clientes a chegarem até sua empresa com rotas automáticas no Google Maps ao escanear."},
        "ru": {"title": "Генератор QR кодов для Google Maps с логотипом | MyLogoQR", "desc": "Создайте QR код с геолокацией вашего магазина или офиса. Быстрый запуск навигатора в Google Maps и Яндекс.", "h1": "Генератор QR кодов для Google Maps с логотипом", "sub": "Направляйте клиентов прямо к дверям вашего заведения с точным маршрутом в навигаторе."},
        "it": {"title": "Generatore Codice QR per Google Maps con Logo Gratis | MyLogoQR", "desc": "Crea codici QR per la posizione della tua attività commerciale. Avvia la navigazione GPS diretta su Google Maps.", "h1": "Generatore Codice QR per Google Maps con Logo", "sub": "Guida clienti e ospiti fino al tuo negozio o ufficio con indicazioni stradali immediate."}
    },
    {
        "slug": "restaurant-menu-qr-code-generator",
        "icon": "🍽️",
        "es": {"title": "Generador de Códigos QR para Menú de Restaurante con Logo | MyLogoQR", "desc": "Crea códigos QR modernos para cartas y menús digitales en PDF o web. Resistentes al desgaste y con el logo de tu restaurante.", "h1": "Generador de Códigos QR para Menús y Cartas con Logo", "sub": "Permite que los comensales vean tu carta digital en sus propios teléfonos al sentarse a la mesa."},
        "pt": {"title": "Gerador de QR Code para Cardápio de Restaurante com Logo | MyLogoQR", "desc": "Crie QR Codes profissionais para cardápios digitais e menus em PDF com a identidade do seu restaurante ou bar.", "h1": "Gerador de QR Code para Cardápio de Restaurante com Logo", "sub": "Permita que seus clientes acessem o menu completo pelo celular assim que se sentarem à mesa."},
        "ru": {"title": "Генератор QR кодов для меню ресторана с логотипом | MyLogoQR", "desc": "Создайте удобный QR код для электронного меню ресторана или кафе с фирменным логотипом. Печать на тейбл-тентах и наклейках.", "h1": "Генератор QR кодов для ресторанного меню с логотипом", "sub": "Гости заведения мгновенно открывают онлайн-меню на смартфонах без необходимости листать бумажные буклеты."},
        "it": {"title": "Generatore Codice QR per Menu Ristorante con Logo | MyLogoQR", "desc": "Crea codici QR professionali per il menu digitale del tuo ristorante o bar. Vettoriali in alta risoluzione con il logo del tuo locale.", "h1": "Generatore Codice QR per Menu Ristorante con Logo", "sub": "Offri ai clienti un accesso immediato al menu digitale direttamente dal proprio smartphone al tavolo."}
    },
    {
        "slug": "vcard-qr-code-generator",
        "icon": "📇",
        "es": {"title": "Generador de Códigos QR vCard Tarjeta de Contacto con Logo | MyLogoQR", "desc": "Crea tarjetas de presentación digitales con QR vCard. Guarda teléfono, correo, empresa y redes en la agenda del teléfono con 1 toque.", "h1": "Generador de Códigos QR vCard con Logo", "sub": "Comparte todos tus datos de contacto profesionales al instante sin errores de escritura."},
        "pt": {"title": "Gerador de QR Code vCard Cartão de Visitas Digital com Logo | MyLogoQR", "desc": "Gere cartões de visita digitais em QR Code. Salva nome, telefone, e-mail e cargo diretamente na agenda do smartphone.", "h1": "Gerador de QR Code vCard com Logotipo", "sub": "Faça networking inteligente compartilhando seu contato completo com uma simples leitura de câmera."},
        "ru": {"title": "Генератор QR кодов vCard Электронная визитка с логотипом | MyLogoQR", "desc": "Создайте электронную визитку в формате QR-кода. Сохранение контакта, телефона, email и должности в телефонную книгу в один клик.", "h1": "Генератор QR кодов vCard с логотипом", "sub": "Делитесь контактами на конференциях и встречах: наведите камеру и контакт сразу сохраняется в смартфоне."},
        "it": {"title": "Generatore Codice QR vCard Biglietto da Visita con Logo | MyLogoQR", "desc": "Crea biglietti da visita digitali in formato vCard con logo. Salva telefono, email e azienda direttamente in rubrica.", "h1": "Generatore Codice QR vCard con Logo", "sub": "Scambia i tuoi contatti di lavoro in modo moderno e senza errori di battitura con un semplice tocco."}
    },
    {
        "slug": "business-card-qr-code-generator",
        "icon": "💼",
        "es": {"title": "Generador de Códigos QR para Tarjetas de Presentación con Logo | MyLogoQR", "desc": "Diseña códigos QR profesionales para imprimir en tus tarjetas de visita. Vector SVG nítido y enlace de contacto directo.", "h1": "Generador de Códigos QR para Tarjetas de Presentación", "sub": "Lleva tus tarjetas de visita de papel a la era digital con un escaneo instantáneo hacia tu perfil o portafolio."},
        "pt": {"title": "Gerador de QR Code para Cartão de Visita com Logo | MyLogoQR", "desc": "Crie QR Codes de alta qualidade para imprimir em cartões de visita físicos. Conecta clientes ao seu portfólio ou contato.", "h1": "Gerador de QR Code para Cartões de Visita com Logo", "sub": "Modernize seus cartões de visita tradicionais permitindo que novos contatos acessem seu portfólio instantaneamente."},
        "ru": {"title": "Генератор QR кодов для визитных карточек с логотипом | MyLogoQR", "desc": "Создавайте стильные векторные QR коды для печати на визитках с вашим логотипом. Высокое качество SVG и PNG для полиграфии.", "h1": "Генератор QR кодов для визитных карточек с логотипом", "sub": "Объедините классические бумажные визитки с вашим онлайн-профилем или сайтом с помощью четкого QR-кода."},
        "it": {"title": "Generatore Codice QR per Biglietti da Visita con Logo | MyLogoQR", "desc": "Progetta codici QR ad alta definizione per la stampa sui tuoi biglietti da visita. Esportazione vettoriale SVG perfetta.", "h1": "Generatore Codice QR per Biglietti da Visita con Logo", "sub": "Collega il tuo biglietto da visita cartaceo al tuo sito web, profilo LinkedIn o catalogo digitale con una scansione."}
    },
    {
        "slug": "youtube-qr-code-generator",
        "icon": "▶️",
        "es": {"title": "Generador de Códigos QR para YouTube con Logo Gratis | MyLogoQR", "desc": "Genera códigos QR personalizados para canales, vídeos o listas de reproducción de YouTube con tu logo. PNG y SVG de alta resolución.", "h1": "Generador de Códigos QR para YouTube con Logo", "sub": "Aumenta tus suscriptores y visualizaciones en YouTube conectando audiencias presenciales directo a tus vídeos."},
        "pt": {"title": "Gerador de QR Code para YouTube com Logo Grátis | MyLogoQR", "desc": "Crie QR Codes para canais, vídeos e shorts do YouTube com o logotipo do seu canal. Downloads grátis em PNG e SVG.", "h1": "Gerador de QR Code para YouTube com Logotipo", "sub": "Ganhe mais inscritos e visualizações levando o público físico direto para seus vídeos no YouTube."},
        "ru": {"title": "Генератор QR кодов для YouTube с логотипом | MyLogoQR", "desc": "Создайте красивый QR код для YouTube канала, видео или плейлиста с логотипом. Векторная печать в высоком разрешении.", "h1": "Генератор QR кодов для YouTube с логотипом", "sub": "Привлекайте зрителей и подписчиков на свой YouTube канал прямо с печатных материалов, плакатов и футболок."},
        "it": {"title": "Generatore Codice QR per YouTube con Logo Gratis | MyLogoQR", "desc": "Crea codici QR personalizzati per canali, video e playlist YouTube con logo. Download gratuiti in formato PNG e SVG.", "h1": "Generatore Codice QR per YouTube con Logo", "sub": "Aumenta le visualizzazioni e gli iscritti al tuo canale YouTube con un codice QR accattivante e professionale."}
    },
    {
        "slug": "facebook-qr-code-generator",
        "icon": "👥",
        "es": {"title": "Generador de Códigos QR para Facebook con Logo | MyLogoQR", "desc": "Crea códigos QR directos para tu página comercial, grupo o evento de Facebook con tu logo. Gratis y permanente.", "h1": "Generador de Códigos QR para Facebook con Logo", "sub": "Aumenta los me gusta y seguidores en tu página de Facebook con un código QR escaneable en tu local o empaques."},
        "pt": {"title": "Gerador de QR Code para Facebook com Logo Grátis | MyLogoQR", "desc": "Gere QR Codes para páginas, grupos e eventos do Facebook com a logo da sua marca. Seguro, gratuito e sem expiração.", "h1": "Gerador de QR Code para Facebook com Logotipo", "sub": "Conquiste mais curtidas e engajamento na sua página comercial do Facebook com escaneamento rápido."},
        "ru": {"title": "Генератор QR кодов для Facebook с логотипом | MyLogoQR", "desc": "Создайте QR код для публичной страницы, группы или события в Facebook с логотипом. Быстрый переход в приложение.", "h1": "Генератор QR кодов для Facebook с логотипом", "sub": "Увеличивайте аудиторию вашей страницы в Facebook с помощью фирменных печатных материалов и витрин."},
        "it": {"title": "Generatore Codice QR per Facebook con Logo Gratis | MyLogoQR", "desc": "Crea codici QR personalizzati per pagine aziendali, gruppi o eventi Facebook con il tuo logo. File pronti per la stampa.", "h1": "Generatore Codice QR per Facebook con Logo", "sub": "Aumenta i follower e le interazioni sulla tua pagina Facebook con un codice QR posizionato nel tuo punto vendita."}
    },
    {
        "slug": "tiktok-qr-code-generator",
        "icon": "🎵",
        "es": {"title": "Generador de Códigos QR para TikTok con Logo Gratis | MyLogoQR", "desc": "Crea códigos QR atractivos para tu perfil de TikTok o vídeos virales con logo. Abre la app de TikTok directamente.", "h1": "Generador de Códigos QR para TikTok con Logo", "sub": "Haz crecer tu comunidad en TikTok llevando espectadores del mundo real directo a tu contenido viral."},
        "pt": {"title": "Gerador de QR Code para TikTok com Logo Grátis | MyLogoQR", "desc": "Gere QR Codes para seu perfil ou vídeos no TikTok com o seu logo. Abre diretamente o aplicativo no celular.", "h1": "Gerador de QR Code para TikTok com Logotipo", "sub": "Atraia mais seguidores no TikTok colocando seu QR Code em embalagens, roupas e eventos presenciais."},
        "ru": {"title": "Генератор QR кодов для TikTok с логотипом | MyLogoQR", "desc": "Создайте стильный QR код со ссылкой на ваш профиль в TikTok или вирусное видео с логотипом. Мгновенный переход в приложение.", "h1": "Генератор QR кодов для TikTok с логотипом", "sub": "Набирайте подписчиков и просмотры в TikTok прямо из реального мира с помощью быстрого сканирования."},
        "it": {"title": "Generatore Codice QR per TikTok con Logo Gratis | MyLogoQR", "desc": "Crea codici QR personalizzati per il tuo profilo o video TikTok con il tuo logo. Apre direttamente l'app TikTok.", "h1": "Generatore Codice QR per TikTok con Logo", "sub": "Fai crescere il tuo pubblico su TikTok indirizzando fan e clienti direttamente al tuo profilo con una scansione."}
    },
    {
        "slug": "telegram-qr-code-generator",
        "icon": "✈️",
        "es": {"title": "Generador de Códigos QR para Telegram con Logo | MyLogoQR", "desc": "Genera códigos QR directos para canales, grupos o chats privados de Telegram con logo. Conexión rápida sin intermediarios.", "h1": "Generador de Códigos QR para Telegram con Logo", "sub": "Haz crecer tu canal o comunidad de Telegram con un escaneo rápido que abre la aplicación de inmediato."},
        "pt": {"title": "Gerador de QR Code para Telegram com Logo Grátis | MyLogoQR", "desc": "Crie QR Codes para canais e grupos do Telegram com sua identidade visual. Entrada rápida e segura na comunidade.", "h1": "Gerador de QR Code para Telegram com Logotipo", "sub": "Facilite a entrada de novos membros no seu canal do Telegram com um QR Code bonito e profissional."},
        "ru": {"title": "Генератор QR кодов для Telegram с логотипом | MyLogoQR", "desc": "Создайте QR код для Telegram-канала, группы или бота с логотипом. Мгновенная подписка и переход в приложение Telegram.", "h1": "Генератор QR кодов для Telegram с логотипом", "sub": "Развивайте свой Telegram канал или бизнес-бота, размещая сканируемые QR коды на визитках, баннерах и товарах."},
        "it": {"title": "Generatore Codice QR per Telegram con Logo | MyLogoQR", "desc": "Crea codici QR personalizzati per canali e gruppi Telegram con logo. Accesso immediato alla community senza passaggi inutili.", "h1": "Generatore Codice QR per Telegram con Logo", "sub": "Invita nuovi membri nel tuo canale Telegram con un codice QR moderno ed elegante."}
    },
    {
        "slug": "spotify-qr-code-generator",
        "icon": "🎧",
        "es": {"title": "Generador de Códigos QR para Spotify con Logo | MyLogoQR", "desc": "Crea códigos QR personalizados para canciones, álbumes y playlists de Spotify con tu logo. Abre la app de Spotify al escanear.", "h1": "Generador de Códigos QR para Spotify con Logo", "sub": "Comparte tu música y playlists favoritas con fans en pósteres de conciertos y álbumes físicos."},
        "pt": {"title": "Gerador de QR Code para Spotify com Logo | MyLogoQR", "desc": "Gere QR Codes para músicas, álbuns e playlists no Spotify com o logo da banda ou marca. Abre o Spotify direto.", "h1": "Gerador de QR Code para Spotify com Logotipo", "sub": "Compartilhe suas faixas e podcasts com ouvintes imprimindo códigos QR em capas e cartazes de eventos."},
        "ru": {"title": "Генератор QR кодов для Spotify с логотипом | MyLogoQR", "desc": "Создайте музыкальный QR код для трека, альбома или плейлиста в Spotify с логотипом. Быстрое воспроизведение в приложении.", "h1": "Генератор QR кодов для Spotify с логотипом", "sub": "Делитесь своими треками и подкастами со слушателями через афиши, мерч и полиграфию."},
        "it": {"title": "Generatore Codice QR per Spotify con Logo | MyLogoQR", "desc": "Crea codici QR per brani, album e playlist su Spotify con il tuo logo. Avvia l'ascolto immediato nell'app Spotify.", "h1": "Generatore Codice QR per Spotify con Logo", "sub": "Condividi la tua musica e le tue playlist con fan e ascoltatori stampando codici QR su locandine e merchandising."}
    },
    {
        "slug": "linkedin-qr-code-generator",
        "icon": "💼",
        "es": {"title": "Generador de Códigos QR para LinkedIn con Logo | MyLogoQR", "desc": "Crea códigos QR para tu perfil profesional o página de empresa en LinkedIn. Ideal para ferias de empleo y conferencias.", "h1": "Generador de Códigos QR para LinkedIn con Logo", "sub": "Conecta con colegas y reclutadores en eventos presenciales sin tener que deletrear tu nombre."},
        "pt": {"title": "Gerador de QR Code para LinkedIn com Logo | MyLogoQR", "desc": "Crie QR Codes para seu perfil ou página de empresa no LinkedIn com logo corporativo. Perfeito para eventos de negócios.", "h1": "Gerador de QR Code para LinkedIn com Logo", "sub": "Expanda sua rede profissional em conferências e palestras permitindo conexões imediatas no LinkedIn."},
        "ru": {"title": "Генератор QR кодов для LinkedIn с логотипом | MyLogoQR", "desc": "Создайте QR код для вашего делового профиля или страницы компании в LinkedIn с логотипом. Идеально для нетворкинга.", "h1": "Генератор QR кодов для LinkedIn с логотипом", "sub": "Устанавливайте деловые связи на выставках и конференциях в одно касание камеры смартфона."},
        "it": {"title": "Generatore Codice QR per LinkedIn con Logo | MyLogoQR", "desc": "Crea codici QR per il tuo profilo personale o pagina aziendale su LinkedIn con logo. Ideale per fiere e conferenze di settore.", "h1": "Generatore Codice QR per LinkedIn con Logo", "sub": "Fai networking professionale di alto livello consentendo a colleghi e clienti di collegarsi subito su LinkedIn."}
    },
    {
        "slug": "paypal-qr-code-generator",
        "icon": "💳",
        "es": {"title": "Generador de Códigos QR para Pagos PayPal con Logo | MyLogoQR", "desc": "Genera códigos QR de pago seguro con PayPal y tu logo. Cobra productos, servicios y donaciones al instante.", "h1": "Generador de Códigos QR para Pagos PayPal con Logo", "sub": "Facilita cobros sin contacto y donaciones seguras a través de tu enlace PayPal.Me personalizado."},
        "pt": {"title": "Gerador de QR Code para Pagamentos PayPal com Logo | MyLogoQR", "desc": "Crie QR Codes para receber pagamentos e doações pelo PayPal com sua logo. Cobranças rápidas e sem contato.", "h1": "Gerador de QR Code para Pagamentos PayPal com Logo", "sub": "Receba pagamentos de clientes de forma segura e imediata exibindo seu código QR no balcão ou fatura."},
        "ru": {"title": "Генератор QR кодов для платежей PayPal с логотипом | MyLogoQR", "desc": "Создайте безопасный QR код для приема платежей и донатов через PayPal с вашим логотипом. Быстрая оплата в один клик.", "h1": "Генератор QR кодов для платежей PayPal с логотипом", "sub": "Принимайте бесконтактную оплату за товары и услуги через ссылку PayPal.Me без кассового оборудования."},
        "it": {"title": "Generatore Codice QR per Pagamenti PayPal con Logo | MyLogoQR", "desc": "Genera codici QR per ricevere pagamenti sicuri tramite PayPal con il tuo logo. Incassa vendite e donazioni senza contatto.", "h1": "Generatore Codice QR per Pagamenti PayPal con Logo", "sub": "Semplifica i pagamenti nel tuo negozio o per le tue consulenze tramite il tuo link PayPal.Me personalizzato."}
    },
    {
        "slug": "pdf-qr-code-generator",
        "icon": "📄",
        "es": {"title": "Generador de Códigos QR para Documentos PDF con Logo | MyLogoQR", "desc": "Crea códigos QR directos a manuales, folletos, catálogos y libros en formato PDF. Descarga vectorial para impresión.", "h1": "Generador de Códigos QR para Documentos PDF con Logo", "sub": "Reemplaza manuales impresos pesados con un código QR limpio que abre tu documento PDF al instante."},
        "pt": {"title": "Gerador de QR Code para Documentos PDF com Logo | MyLogoQR", "desc": "Gere QR Codes com link direto para manuais, catálogos e folhetos em PDF. Econômico, sustentável e profissional.", "h1": "Gerador de QR Code para Documentos PDF com Logo", "sub": "Compartilhe catálogos de produtos e documentos importantes com um simples escaneamento de celular."},
        "ru": {"title": "Генератор QR кодов для PDF документов с логотипом | MyLogoQR", "desc": "Создайте QR код со ссылкой на инструкцию, каталог товаров или буклет в формате PDF с вашим логотипом.", "h1": "Генератор QR кодов для PDF документов с логотипом", "sub": "Замените тяжелые бумажные брошюры на удобный цифровой доступ к PDF-документам для ваших клиентов."},
        "it": {"title": "Generatore Codice QR per Documenti PDF con Logo | MyLogoQR", "desc": "Crea codici QR con link diretto a cataloghi, brochure e manuali d'uso in formato PDF. Ideale per packaging e fiere.", "h1": "Generatore Codice QR per Documenti PDF con Logo", "sub": "Sostituisci i voluminosi libretti cartacei con un codice QR moderno che apre il documento PDF in un istante."}
    },
    {
        "slug": "email-qr-code-generator",
        "icon": "✉️",
        "es": {"title": "Generador de Códigos QR para Enviar Correo con Logo | MyLogoQR", "desc": "Crea códigos QR que abren el cliente de correo con destinatario, asunto y texto predefinidos. 100% libre de errores.", "h1": "Generador de Códigos QR para Correo Electrónico con Logo", "sub": "Recibe consultas de clientes y solicitudes de soporte directamente en tu bandeja de entrada al escanear."},
        "pt": {"title": "Gerador de QR Code para Envio de E-mail com Logo | MyLogoQR", "desc": "Crie QR Codes que abrem o aplicativo de e-mail com endereço, assunto e corpo da mensagem já preenchidos.", "h1": "Gerador de QR Code para E-mail com Logotipo", "sub": "Receba pedidos de orçamento e dúvidas de clientes diretamente no seu e-mail corporativo sem erros de digitação."},
        "ru": {"title": "Генератор QR кодов для отправки Email с логотипом | MyLogoQR", "desc": "Создайте QR код для отправки электронного письма с заполненным адресом, темой и текстом. Быстрый контакт с клиентом.", "h1": "Генератор QR кодов для Email с логотипом", "sub": "Клиенты мгновенно открывают почтовую программу с готовым письмом в ваш отдел продаж или поддержку."},
        "it": {"title": "Generatore Codice QR per Invio Email con Logo | MyLogoQR", "desc": "Crea codici QR che aprono l'app di posta elettronica con indirizzo, oggetto e testo precompilati. Facile e senza errori.", "h1": "Generatore Codice QR per Email con Logo", "sub": "Ricevi richieste di preventivo e supporto direttamente nella tua casella di posta elettronica con una scansione."}
    },
    {
        "slug": "sms-qr-code-generator",
        "icon": "📱",
        "es": {"title": "Generador de Códigos QR para Mensajes SMS con Logo | MyLogoQR", "desc": "Genera códigos QR que preparan un mensaje de texto SMS con número y contenido listos para enviar en un clic.", "h1": "Generador de Códigos QR para Mensajes SMS con Logo", "sub": "Excelente para confirmaciones de citas, votaciones y suscripciones a promociones por mensaje de texto."},
        "pt": {"title": "Gerador de QR Code para Envio de SMS com Logo | MyLogoQR", "desc": "Crie QR Codes que abrem o app de SMS com número de destino e texto prontos para enviar. Seguro e universal.", "h1": "Gerador de QR Code para SMS com Logotipo", "sub": "Perfeito para confirmação de agendamentos, promoções e atendimento rápido via mensagem de texto."},
        "ru": {"title": "Генератор QR кодов для отправки SMS с логотипом | MyLogoQR", "desc": "Создайте QR код для отправки SMS сообщения на заданный номер с готовым текстом. Работает на всех телефонах.", "h1": "Генератор QR кодов для SMS с логотипом", "sub": "Удобно для подтверждения записи, регистрации на акции и быстрой связи без подключения к интернету."},
        "it": {"title": "Generatore Codice QR per Invio SMS con Logo | MyLogoQR", "desc": "Crea codici QR che preparano un messaggio SMS con numero di telefono e testo predefiniti pronti per l'invio.", "h1": "Generatore Codice QR per SMS con Logo", "sub": "Ideale per conferme di prenotazioni, adesioni a promozioni e comunicazioni rapide via messaggio di testo."}
    },
    {
        "slug": "text-qr-code-generator",
        "icon": "📝",
        "es": {"title": "Generador de Códigos QR de Texto Plano con Logo | MyLogoQR", "desc": "Codifica texto sin conexión a internet en códigos QR estáticos. Notas, claves seriales, contraseñas y mensajes privados.", "h1": "Generador de Códigos QR de Texto con Logo", "sub": "Almacena información directamente dentro de los píxeles del código QR. Funciona 100% offline y nunca caduca."},
        "pt": {"title": "Gerador de QR Code de Texto Simples com Logo | MyLogoQR", "desc": "Gere QR Codes estáticos com texto simples que funcionam totalmente offline. Seguro, privado e permanente.", "h1": "Gerador de QR Code de Texto com Logotipo", "sub": "Guarde anotações, números de série e instruções diretamente no padrão de pixels do QR Code sem internet."},
        "ru": {"title": "Генератор QR кодов для обычного текста с логотипом | MyLogoQR", "desc": "Кодируйте произвольный текст в статический QR код. Работает полностью офлайн без серверов и интернета.", "h1": "Генератор QR кодов для текста с логотипом", "sub": "Текст сохраняется непосредственно в пикселях штрихкода: заметки, серийные номера и пароли открываются мгновенно."},
        "it": {"title": "Generatore Codice QR di Testo Semplice con Logo | MyLogoQR", "desc": "Codifica testo puro in un codice QR statico che funziona anche senza connessione internet. Privato e sicuro al 100%.", "h1": "Generatore Codice QR di Testo con Logo", "sub": "Memorizza istruzioni, numeri di serie e note direttamente nel pattern del QR code in modo permanente e offline."}
    },
    {
        "slug": "app-store-qr-code-generator",
        "icon": "📲",
        "es": {"title": "Generador de Códigos QR para App Store y Google Play | MyLogoQR", "desc": "Crea códigos QR directos para descargar tu aplicación móvil en iOS App Store y Google Play Store con logo.", "h1": "Generador de Códigos QR para Descarga de Apps con Logo", "sub": "Multiplica las instalaciones de tu aplicación móvil permitiendo que los usuarios descarguen en un segundo."},
        "pt": {"title": "Gerador de QR Code para App Store e Google Play com Logo | MyLogoQR", "desc": "Gere QR Codes para download de aplicativos na Apple App Store e Google Play Store com o ícone do seu app.", "h1": "Gerador de QR Code para Apps com Logotipo", "sub": "Aumente as instalações do seu aplicativo móvel com um código QR bonito estampado em seus materiais promocionais."},
        "ru": {"title": "Генератор QR кодов для App Store и Google Play | MyLogoQR", "desc": "Создайте QR код со ссылкой на скачивание мобильного приложения в App Store и Google Play с вашим логотипом.", "h1": "Генератор QR кодов для приложений App Store и Google Play", "sub": "Увеличивайте количество установок вашего приложения, размещая сканируемый QR код в наружной рекламе и на сайте."},
        "it": {"title": "Generatore Codice QR per App Store e Google Play con Logo | MyLogoQR", "desc": "Crea codici QR per il download della tua app mobile su App Store e Google Play con il logo ufficiale.", "h1": "Generatore Codice QR per Download App con Logo", "sub": "Incrementa i download della tua applicazione per smartphone con un codice QR elegante posizionato sui tuoi banner."}
    },
    {
        "slug": "real-estate-qr-code-generator",
        "icon": "🏠",
        "es": {"title": "Generador de Códigos QR para Inmobiliarias y Bienes Raíces | MyLogoQR", "desc": "Crea códigos QR de alta resolución para carteles de venta, tours virtuales 3D y fichas de propiedades inmobiliarias.", "h1": "Generador de Códigos QR para Bienes Raíces con Logo", "sub": "Permite que compradores interesados vean fotos, precios y detalles de la propiedad directamente desde la acera."},
        "pt": {"title": "Gerador de QR Code para Imobiliárias e Corretores com Logo | MyLogoQR", "desc": "Gere QR Codes para placas de imóveis, tours virtuais e fichas de venda com o logotipo da sua imobiliária.", "h1": "Gerador de QR Code para Mercado Imobiliário com Logo", "sub": "Facilite o acesso a fotos e valores de imóveis para clientes que passam em frente à placa de venda."},
        "ru": {"title": "Генератор QR кодов для недвижимости и риелторов с логотипом | MyLogoQR", "desc": "Создайте QR коды для вывесок о продаже недвижимости, виртуальных туров 3D и каталогов квартир с логотипом агентства.", "h1": "Генератор QR кодов для недвижимости с логотипом", "sub": "Позвольте потенциальным покупателям мгновенно увидеть планировку, цену и фото объекта прямо с уличного баннера."},
        "it": {"title": "Generatore Codice QR per Agenzie Immobiliari con Logo | MyLogoQR", "desc": "Crea codici QR per cartelli di vendita immobili, tour virtuali 3D e schede tecniche con il logo della tua agenzia.", "h1": "Generatore Codice QR per Immobiliari con Logo", "sub": "Consenti ai potenziali acquirenti di consultare foto, planimetrie e prezzi dell'immobile direttamente dal cartello."}
    },
    {
        "slug": "wedding-qr-code-generator",
        "icon": "💍",
        "es": {"title": "Generador de Códigos QR para Invitaciones de Boda con Logo | MyLogoQR", "desc": "Crea elegantes códigos QR para confirmaciones de asistencia (RSVP), lista de regalos y ubicación de la ceremonia.", "h1": "Generador de Códigos QR para Invitaciones de Boda", "sub": "Añade un toque moderno y sofisticado a tus invitaciones de boda en papel con un código QR personalizado."},
        "pt": {"title": "Gerador de QR Code para Convites de Casamento com Logo | MyLogoQR", "desc": "Crie QR Codes sofisticados para confirmação de presença (RSVP), lista de presentes e localização da cerimônia.", "h1": "Gerador de QR Code para Convites de Casamento", "sub": "Torne seus convites de casamento interativos e elegantes facilitando o RSVP e rotas para os convidados."},
        "ru": {"title": "Генератор QR кодов для свадебных приглашений с логотипом | MyLogoQR", "desc": "Создайте изысканные QR коды для свадебных пригласительных: подтверждение присутствия, список подарков и карта проезда.", "h1": "Генератор QR кодов для свадебных приглашений", "sub": "Добавьте изящный штрих к вашим свадебным открыткам: гости подтверждают визит и смотрят маршрут в один клик."},
        "it": {"title": "Generatore Codice QR per Inviti di Nozze con Logo | MyLogoQR", "desc": "Crea eleganti codici QR per partecipazioni di matrimonio: conferma presenza (RSVP), lista nozze e mappa della cerimonia.", "h1": "Generatore Codice QR per Partecipazioni di Nozze", "sub": "Aggiungi un dettaglio moderno ed esclusivo ai tuoi inviti di nozze cartacei con un codice QR personalizzato."}
    }
]

def generate_multilingual_network():
    print("[Starting] Programmatic Multi-Language Network Generation...")
    
    # 1. Update English HTML files: add hreflang + language switchers
    update_english_pages()

    # 2. For each language, generate localized directory and files
    for lang_code in ["es", "pt", "ru", "it"]:
        lang_dir = os.path.join(WEBSITE_DIR, lang_code)
        os.makedirs(lang_dir, exist_ok=True)
        print(f"\n--- Processing Language: {lang_code.upper()} ({lang_dir}) ---")

        # Generate localized index.html
        generate_localized_home(lang_code, lang_dir)

        # Generate localized qr-code-types.html
        generate_localized_hub(lang_code, lang_dir)

        # Generate all 22 localized tools
        for tool in ALL_TOOLS:
            generate_localized_tool(lang_code, lang_dir, tool)

    # 3. Update .htaccess with rewrite rules
    update_htaccess()

    # 4. Update sitemap.xml with all new URLs
    update_sitemap()

    print("\n[Complete] Successfully generated 96 localized pages across 4 languages!")

def update_english_pages():
    print("[Updating English Pages with hreflang and Language Switchers]...")
    for root, dirs, files in os.walk(WEBSITE_DIR):
        if "tests" in root or "scripts" in root or any(x in root for x in ["\\es", "\\pt", "\\ru", "\\it"]):
            continue
        for f in files:
            if not f.endswith(".html") or "google41b2cdf" in f:
                continue
            fpath = os.path.join(root, f)
            rel = os.path.relpath(fpath, WEBSITE_DIR)
            
            with open(fpath, "r", encoding="utf-8") as fp:
                c = fp.read()

            modified = False

            # Determine slug path
            slug_path = ""
            if f != "index.html":
                slug_path = f.replace(".html", "")
                if "blog" in rel:
                    slug_path = f"blog/{f.replace('.html', '')}"

            # 1. Add hreflang tags if not present
            if 'hreflang="es"' not in c and "</head>" in c:
                hreflang_html = get_hreflang_tags(slug_path)
                c = c.replace("</head>", f"{hreflang_html}\n</head>")
                modified = True

            # 2. Add language switcher to Header
            if 'class="lang-switch"' not in c and '</nav>' in c:
                lang_switcher = get_lang_switcher_header("en", slug_path)
                c = re.sub(r'(<nav id="nav"[^>]*>.*?)(</nav>)', rf'\1{lang_switcher}\2', c, flags=re.DOTALL)
                modified = True

            # 3. Add language strip to Footer
            if 'class="lang-bar"' not in c and '<div class="copy"' in c:
                lang_strip = get_lang_strip_footer("en", slug_path)
                c = c.replace('<div class="copy"', f'{lang_strip}\n <div class="copy"')
                modified = True

            if modified:
                with open(fpath, "w", encoding="utf-8") as fp:
                    fp.write(c)

def generate_localized_home(lang_code, lang_dir):
    src_path = os.path.join(WEBSITE_DIR, "index.html")
    dest_path = os.path.join(lang_dir, "index.html")
    with open(src_path, "r", encoding="utf-8") as f:
        c = f.read()

    meta = LANGUAGES[lang_code]

    # HTML lang
    c = re.sub(r'<html lang="[^"]+"', f'<html lang="{meta["lang_code"]}"', c)

    # Title & Meta Description
    c = re.sub(r'<title>.*?</title>', f'<title>{meta["home_title"]}</title>', c)
    c = re.sub(r'<meta name="description" content="[^"]+"', f'<meta name="description" content="{meta["home_desc"]}"', c)
    c = re.sub(r'<link rel="canonical" href="[^"]+"', f'<link rel="canonical" href="https://mylogoqr.com/{lang_code}/"', c)

    # Hreflang
    hreflangs = get_hreflang_tags("")
    if 'hreflang="es"' in c:
        c = re.sub(r'<link rel="alternate" hreflang=.*?>', '', c)
    c = c.replace("</head>", f"{hreflangs}\n</head>")

    # Nav
    c = c.replace('>Generators</a>', f'>{meta["header_gen"]}</a>')
    c = c.replace('>How to Use</a>', f'>{meta["header_use"]}</a>')
    c = c.replace('>Blog</a>', f'>{meta["header_blog"]}</a>')
    c = c.replace('>FAQ</a>', f'>{meta["header_faq"]}</a>')
    c = c.replace('>About</a>', f'>{meta["header_about"]}</a>')
    c = c.replace('>Contact</a>', f'>{meta["header_contact"]}</a>')
    c = c.replace('>Create QR</a>', f'>{meta["header_cta"]}</a>')

    # Hero
    c = re.sub(r'<h1[^>]*>.*?</h1>', f'<h1>{meta["home_h1"]}</h1>', c, count=1, flags=re.DOTALL)
    c = re.sub(r'<p class="sub"[^>]*>.*?</p>', f'<p class="sub">{meta["home_sub"]}</p>', c, count=1, flags=re.DOTALL)
    c = re.sub(r'<section class="hero".*?<div class="chips">', f'<section class="hero"><div class="wrap bar" style="display:none"></div><h1>{meta["home_h1"]}</h1><p style="color:#E2E8F0;font-size:1.15rem;margin:16px auto 0;max-width:60ch">{meta["home_sub"]}</p><div class="chips">', c, flags=re.DOTALL)

    # Chips
    for old_chip, new_chip in zip(["Runs in your browser", "Never expires", "Unlimited scans", "PNG and SVG"], meta["chips"]):
        c = c.replace(f'<li>{old_chip}</li>', f'<li>{new_chip}</li>')

    # Generator UI
    c = c.replace('1. Your content', meta["ui_your_content"])
    c = c.replace('2. Quick styles', meta["ui_quick_styles"])
    c = c.replace('3. Colors', meta["ui_colors"])
    c = c.replace('Dots color', meta["ui_dots_color"])
    c = c.replace('Background', meta["ui_bg_color"])
    c = c.replace('4. Logo', meta["ui_logo"])
    c = c.replace('Upload logo', meta["ui_upload_logo"])
    c = c.replace('Logo size', meta["ui_logo_size"])
    c = c.replace('Download PNG', meta["ui_download_png"])
    c = c.replace('Download SVG', meta["ui_download_svg"])

    # Footer
    c = re.sub(r'<p style="font-size:0.92rem;line-height:1.65;color:#94A3B8;max-width:320px;margin-top:8px">.*?</p>', f'<p style="font-size:0.92rem;line-height:1.65;color:#94A3B8;max-width:320px;margin-top:8px">{meta["footer_desc"]}</p>', c, flags=re.DOTALL)
    c = c.replace('<h4>Generators</h4>', f'<h4>{meta["footer_col_gen"]}</h4>')
    c = c.replace('<h4>Resources</h4>', f'<h4>{meta["footer_col_res"]}</h4>')
    c = c.replace('<h4>Trust & Legal</h4>', f'<h4>{meta["footer_col_legal"]}</h4>')
    c = c.replace('All Generators Hub', meta["footer_hub"])
    c = c.replace('Guides & Blog', meta["footer_guides"])
    c = c.replace('About Us', meta["footer_about"])
    c = c.replace('Contact Support', meta["footer_contact"])
    c = c.replace('Privacy Policy', meta["footer_privacy"])
    c = c.replace('Terms of Service', meta["footer_terms"])
    c = c.replace('Cookie Policy', meta["footer_cookie"])
    c = c.replace('Disclaimer', meta["footer_disclaimer"])
    c = re.sub(r'<div class="copy"[^>]*>.*?</div>', f'<div class="copy" style="margin-top:14px">{meta["footer_copy"]}</div>', c)

    # Update internal nav links to localized versions
    c = c.replace('href="/qr-code-types"', f'href="/{lang_code}/qr-code-types"')
    c = c.replace('href="/whatsapp-qr-code-generator"', f'href="/{lang_code}/whatsapp-qr-code-generator"')
    c = c.replace('href="/wifi-qr-code-generator"', f'href="/{lang_code}/wifi-qr-code-generator"')
    c = c.replace('href="/instagram-qr-code-generator"', f'href="/{lang_code}/instagram-qr-code-generator"')
    c = c.replace('href="/google-reviews-qr-code-generator"', f'href="/{lang_code}/google-reviews-qr-code-generator"')
    c = c.replace('href="/vcard-qr-code-generator"', f'href="/{lang_code}/vcard-qr-code-generator"')
    c = c.replace('href="/restaurant-menu-qr-code-generator"', f'href="/{lang_code}/restaurant-menu-qr-code-generator"')

    # Switchers
    header_switcher = get_lang_switcher_header(lang_code, "")
    footer_strip = get_lang_strip_footer(lang_code, "")
    c = re.sub(r'<div class="lang-switch".*?</div>', header_switcher, c)
    c = re.sub(r'<div class="lang-bar".*?</div>', footer_strip, c, flags=re.DOTALL)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(c)
    print(f"  [Created] {lang_code}/index.html")

def generate_localized_hub(lang_code, lang_dir):
    src_path = os.path.join(WEBSITE_DIR, "qr-code-types.html")
    dest_path = os.path.join(lang_dir, "qr-code-types.html")
    with open(src_path, "r", encoding="utf-8") as f:
        c = f.read()

    meta = LANGUAGES[lang_code]

    # Lang & Canonical
    c = re.sub(r'<html lang="[^"]+"', f'<html lang="{meta["lang_code"]}"', c)
    c = re.sub(r'<title>.*?</title>', f'<title>{meta["hub_title"]}</title>', c)
    c = re.sub(r'<meta name="description" content="[^"]+"', f'<meta name="description" content="{meta["hub_desc"]}"', c)
    c = re.sub(r'<link rel="canonical" href="[^"]+"', f'<link rel="canonical" href="https://mylogoqr.com/{lang_code}/qr-code-types"', c)

    # Hreflang
    hreflangs = get_hreflang_tags("qr-code-types")
    c = c.replace("</head>", f"{hreflangs}\n</head>")

    # Hero
    c = re.sub(r'<h1[^>]*>.*?</h1>', f'<h1>{meta["hub_h1"]}</h1>', c, count=1, flags=re.DOTALL)
    c = re.sub(r'<p class="sub"[^>]*>.*?</p>', f'<p class="sub">{meta["hub_sub"]}</p>', c, count=1, flags=re.DOTALL)

    # Nav
    c = c.replace('>Generators</a>', f'>{meta["header_gen"]}</a>')
    c = c.replace('>How to Use</a>', f'>{meta["header_use"]}</a>')
    c = c.replace('>Blog</a>', f'>{meta["header_blog"]}</a>')
    c = c.replace('>FAQ</a>', f'>{meta["header_faq"]}</a>')
    c = c.replace('>About</a>', f'>{meta["header_about"]}</a>')
    c = c.replace('>Contact</a>', f'>{meta["header_contact"]}</a>')
    c = c.replace('>Create QR</a>', f'>{meta["header_cta"]}</a>')

    # Update all tool card links to localized versions
    for tool in ALL_TOOLS:
        slug = tool["slug"]
        c = c.replace(f'href="/{slug}"', f'href="/{lang_code}/{slug}"')
        # Localize card title if available
        if lang_code in tool:
            t_data = tool[lang_code]
            # Replace card h3 title
            c = re.sub(rf'(href="/{lang_code}/{slug}"[^>]*>.*?<h3>)(.*?)(</h3>)', rf'\1{t_data["h1"]}\3', c, flags=re.DOTALL)

    # Switchers
    header_switcher = get_lang_switcher_header(lang_code, "qr-code-types")
    footer_strip = get_lang_strip_footer(lang_code, "qr-code-types")
    if 'class="lang-switch"' in c:
        c = re.sub(r'<div class="lang-switch".*?</div>', header_switcher, c)
    else:
        c = re.sub(r'(<nav id="nav"[^>]*>.*?)(</nav>)', rf'\1{header_switcher}\2', c, flags=re.DOTALL)

    if 'class="lang-bar"' in c:
        c = re.sub(r'<div class="lang-bar".*?</div>', footer_strip, c, flags=re.DOTALL)
    else:
        c = c.replace('<div class="copy"', f'{footer_strip}\n <div class="copy"')

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(c)
    print(f"  [Created] {lang_code}/qr-code-types.html")

def generate_localized_tool(lang_code, lang_dir, tool):
    slug = tool["slug"]
    src_path = os.path.join(WEBSITE_DIR, f"{slug}.html")
    if not os.path.exists(src_path):
        return

    dest_path = os.path.join(lang_dir, f"{slug}.html")
    with open(src_path, "r", encoding="utf-8") as f:
        c = f.read()

    meta = LANGUAGES[lang_code]
    tool_data = tool.get(lang_code, {})
    if not tool_data:
        # Fallback to English
        tool_data = {
            "title": f"Custom {slug.replace('-', ' ').title()} with Logo | MyLogoQR",
            "desc": f"Create custom {slug.replace('-', ' ')} with your brand logo.",
            "h1": f"{slug.replace('-', ' ').title()} with Logo",
            "sub": "Generate customized vector QR codes in seconds. 100% free and client-side."
        }

    # Lang & Canonical
    c = re.sub(r'<html lang="[^"]+"', f'<html lang="{meta["lang_code"]}"', c)
    c = re.sub(r'<title>.*?</title>', f'<title>{tool_data["title"]}</title>', c)
    c = re.sub(r'<meta name="description" content="[^"]+"', f'<meta name="description" content="{tool_data["desc"]}"', c)
    c = re.sub(r'<link rel="canonical" href="[^"]+"', f'<link rel="canonical" href="https://mylogoqr.com/{lang_code}/{slug}"', c)

    # Hreflang
    hreflangs = get_hreflang_tags(slug)
    c = c.replace("</head>", f"{hreflangs}\n</head>")

    # Nav
    c = c.replace('>Generators</a>', f'>{meta["header_gen"]}</a>')
    c = c.replace('>How to Use</a>', f'>{meta["header_use"]}</a>')
    c = c.replace('>Blog</a>', f'>{meta["header_blog"]}</a>')
    c = c.replace('>FAQ</a>', f'>{meta["header_faq"]}</a>')
    c = c.replace('>About</a>', f'>{meta["header_about"]}</a>')
    c = c.replace('>Contact</a>', f'>{meta["header_contact"]}</a>')
    c = c.replace('>Create QR</a>', f'>{meta["header_cta"]}</a>')

    # Hero
    c = re.sub(r'<h1[^>]*>.*?</h1>', f'<h1>{tool_data["h1"]}</h1>', c, count=1, flags=re.DOTALL)
    c = re.sub(r'<p class="sub"[^>]*>.*?</p>', f'<p class="sub">{tool_data["sub"]}</p>', c, count=1, flags=re.DOTALL)

    # Generator UI Section Headers
    c = c.replace('1. Your content', meta["ui_your_content"])
    c = c.replace('2. Quick styles', meta["ui_quick_styles"])
    c = c.replace('3. Colors', meta["ui_colors"])
    c = c.replace('Dots color', meta["ui_dots_color"])
    c = c.replace('Background', meta["ui_bg_color"])
    c = c.replace('4. Logo', meta["ui_logo"])
    c = c.replace('Upload logo', meta["ui_upload_logo"])
    c = c.replace('Logo size', meta["ui_logo_size"])
    c = c.replace('Download PNG', meta["ui_download_png"])
    c = c.replace('Download SVG', meta["ui_download_svg"])

    # Localize field labels if specified
    if "field" in tool_data:
        c = re.sub(r'(<label[^>]*>)(.*?)(</label>)', rf'\1{tool_data["field"]}\3', c, count=1)

    # Footer
    c = re.sub(r'<p style="font-size:0.92rem;line-height:1.65;color:#94A3B8;max-width:320px;margin-top:8px">.*?</p>', f'<p style="font-size:0.92rem;line-height:1.65;color:#94A3B8;max-width:320px;margin-top:8px">{meta["footer_desc"]}</p>', c, flags=re.DOTALL)
    c = c.replace('<h4>Generators</h4>', f'<h4>{meta["footer_col_gen"]}</h4>')
    c = c.replace('<h4>Resources</h4>', f'<h4>{meta["footer_col_res"]}</h4>')
    c = c.replace('<h4>Trust & Legal</h4>', f'<h4>{meta["footer_col_legal"]}</h4>')
    c = c.replace('All Generators Hub', meta["footer_hub"])
    c = c.replace('Guides & Blog', meta["footer_guides"])
    c = c.replace('About Us', meta["footer_about"])
    c = c.replace('Contact Support', meta["footer_contact"])
    c = c.replace('Privacy Policy', meta["footer_privacy"])
    c = c.replace('Terms of Service', meta["footer_terms"])
    c = c.replace('Cookie Policy', meta["footer_cookie"])
    c = c.replace('Disclaimer', meta["footer_disclaimer"])
    c = re.sub(r'<div class="copy"[^>]*>.*?</div>', f'<div class="copy" style="margin-top:14px">{meta["footer_copy"]}</div>', c)

    # Localize internal links to stay within language
    c = c.replace('href="/qr-code-types"', f'href="/{lang_code}/qr-code-types"')
    c = c.replace('href="/whatsapp-qr-code-generator"', f'href="/{lang_code}/whatsapp-qr-code-generator"')
    c = c.replace('href="/wifi-qr-code-generator"', f'href="/{lang_code}/wifi-qr-code-generator"')
    c = c.replace('href="/instagram-qr-code-generator"', f'href="/{lang_code}/instagram-qr-code-generator"')
    c = c.replace('href="/google-reviews-qr-code-generator"', f'href="/{lang_code}/google-reviews-qr-code-generator"')
    c = c.replace('href="/vcard-qr-code-generator"', f'href="/{lang_code}/vcard-qr-code-generator"')
    c = c.replace('href="/restaurant-menu-qr-code-generator"', f'href="/{lang_code}/restaurant-menu-qr-code-generator"')

    # Switchers
    header_switcher = get_lang_switcher_header(lang_code, slug)
    footer_strip = get_lang_strip_footer(lang_code, slug)
    if 'class="lang-switch"' in c:
        c = re.sub(r'<div class="lang-switch".*?</div>', header_switcher, c)
    else:
        c = re.sub(r'(<nav id="nav"[^>]*>.*?)(</nav>)', rf'\1{header_switcher}\2', c, flags=re.DOTALL)

    if 'class="lang-bar"' in c:
        c = re.sub(r'<div class="lang-bar".*?</div>', footer_strip, c, flags=re.DOTALL)
    else:
        c = c.replace('<div class="copy"', f'{footer_strip}\n <div class="copy"')

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(c)

def update_htaccess():
    print("\n[Updating .htaccess with Multi-Language Rewrite Rules]...")
    if not os.path.exists(HTACCESS_PATH):
        return

    with open(HTACCESS_PATH, "r", encoding="utf-8") as f:
        ht = f.read()

    multilang_rules = """# 10. Clean URLs for multi-language roots: /es/ -> /es/index.html
RewriteRule ^(es|pt|ru|it)/?$ /$1/index.html [L,NC]

# 11. Clean URLs for multi-language tools: /es/slug -> /es/slug.html
RewriteRule ^(es|pt|ru|it)/([^/.]+)/?$ /$1/$2.html [L,NC]
"""

    if "# 10. Clean URLs for multi-language roots" not in ht:
        # Insert right before `# 10. Clean URL for root tools and pages`
        target = "# 10. Clean URL for root tools and pages: /slug -> /slug.html"
        if target in ht:
            ht = ht.replace(target, f"{multilang_rules}\n# 12. Clean URL for root tools and pages: /slug -> /slug.html")
        else:
            ht = ht + f"\n{multilang_rules}\n"

        with open(HTACCESS_PATH, "w", encoding="utf-8") as f:
            f.write(ht)
        print("  .htaccess updated with multi-language rewrite rules.")

def update_sitemap():
    print("\n[Updating sitemap.xml with Multi-Language URLs]...")
    if not os.path.exists(SITEMAP_PATH):
        return

    with open(SITEMAP_PATH, "r", encoding="utf-8") as f:
        sm = f.read()

    new_urls = []
    today = "2026-10-30"

    for lang_code in ["es", "pt", "ru", "it"]:
        # Language home
        loc_home = f"https://mylogoqr.com/{lang_code}/"
        if f"<loc>{loc_home}</loc>" not in sm:
            new_urls.append(f"""  <url>
    <loc>{loc_home}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
  </url>""")

        # Language hub
        loc_hub = f"https://mylogoqr.com/{lang_code}/qr-code-types"
        if f"<loc>{loc_hub}</loc>" not in sm:
            new_urls.append(f"""  <url>
    <loc>{loc_hub}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.85</priority>
  </url>""")

        # All 22 tools
        for tool in ALL_TOOLS:
            slug = tool["slug"]
            loc_tool = f"https://mylogoqr.com/{lang_code}/{slug}"
            if f"<loc>{loc_tool}</loc>" not in sm:
                new_urls.append(f"""  <url>
    <loc>{loc_tool}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.85</priority>
  </url>""")

    if new_urls:
        insert_block = "\n" + "\n".join(new_urls)
        sm = sm.replace("</urlset>", f"{insert_block}\n</urlset>")
        with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
            f.write(sm)
        print(f"  sitemap.xml updated with {len(new_urls)} new multi-language URLs.")

if __name__ == "__main__":
    generate_multilingual_network()
