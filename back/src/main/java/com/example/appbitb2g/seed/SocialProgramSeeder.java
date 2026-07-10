package com.example.appbitb2g.seed;

import com.example.appbitb2g.model.SocialProgram;
import com.example.appbitb2g.repository.SocialProgramRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Component;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

@Component
@Profile("dev")
public class SocialProgramSeeder {

    @Autowired private SocialProgramRepository repo;

    public void seed() {
        if (repo.count() > 0) return;

        // { nombre, tipo, descripcion, municipio, cluster, organizacion, liderReferente, replicable, impactoEstimado, urlReferencia, fechaInicio, fechaFin, activo }
        Object[][] programs = {

            //  Florianópolis - TRINDADE (many programs)
            {"Programa de Formacion en Tecnologias Web", "FORMACION", "Curso intensivo de HTML, CSS y JavaScript para jovenes de 18 a 25 anos", "Florianopolis", "TRINDADE", "Prefeitura de Florianopolis", null, 1, "ALTO", "https://floripa.gov.br/formacion-web", LocalDate.of(2024, 1, 15), LocalDate.of(2024, 6, 30), true},
            {"Experiencia en Arte Urbano Comunitario", "EXPERIENCIA", "Intervencion artistica en espacios publicos junto a artistas locales", "Florianopolis", "TRINDADE", "Coletivo Arte Viva Floripa", "Bruno Tavares", 1, "BAJO", "https://arteviva.org.br/arte-urbano", LocalDate.of(2024, 4, 1), LocalDate.of(2024, 10, 31), true},
            {"Mentoria en Desarrollo de Juegos", "MENTORIA", "Acompañamiento a desarrolladores indie en creacion de juegos", "Florianopolis", "TRINDADE", "Game Dev Community SC", "Lucas Mendes", 1, "ALTO", "https://gamedevsc.org.br/mentoria", LocalDate.of(2024, 3, 1), null, true},
            {"Curso de Illustrator y Diseño Gráfico", "FORMACION", "Aprender diseño gráfico profesional", "Florianopolis", "TRINDADE", "Escuela de Arte y Diseño Floripa", null, 1, "MEDIO", "https://eadf.com.br/illustrator", LocalDate.of(2024, 2, 15), LocalDate.of(2024, 8, 15), true},
            {"Experiencia en Cine Club Universitario", "EXPERIENCIA", "Organizar proyecciones y charlas con jóvenes", "Florianopolis", "TRINDADE", "Cine Club UFSC", "Mariana Costa", 1, "BAJO", "https://cineclubufsc.org.br", LocalDate.of(2024, 5, 1), null, true},
            {"Curso de React y Next.js", "FORMACION", "Aprender a desarrollar aplicaciones web con React y Next.js", "Florianopolis", "TRINDADE", "Dev Community SC", "Fernanda Souza", 1, "ALTO", "https://devcommunitysc.org.br/react", LocalDate.of(2024, 7, 1), LocalDate.of(2025, 1, 15), true},

            //  Florianópolis - UFSC (many programs)
            {"Curso de Programacion en Python", "FORMACION", "Introduccion a Python y analisis de datos", "Florianopolis", "UFSC", "Universidad Federal de Santa Catarina", null, 0, "ALTO", "https://ufsc.br/cursos/python", LocalDate.of(2024, 1, 10), LocalDate.of(2024, 7, 15), true},
            {"Experiencia en Apoyo a Adultos Mayores", "EXPERIENCIA", "Visitas y actividades recreativas en hogares de ancianos de la region", "Florianopolis", "UFSC", "Instituto Cuidar Florianopolis", "Beatriz Campos", 1, "ALTO", "https://institutocuidar.org.br/adultos-mayores", LocalDate.of(2024, 5, 1), LocalDate.of(2024, 12, 15), true},
            {"Mentoria en Investigación Científica", "MENTORIA", "Acompañamiento a estudiantes en proyectos de investigación", "Florianopolis", "UFSC", "Instituto de Investigaciones UFSC", "Dr. Carlos Alberto", 0, "ALTO", "https://iiufsc.org.br/mentoria-investigacion", LocalDate.of(2024, 3, 1), null, true},
            {"Curso de Machine Learning", "FORMACION", "Introducción a machine learning y modelos predictivos", "Florianopolis", "UFSC", "Departamento de Computación UFSC", null, 0, "ALTO", "https://dc.ufsc.br/ml", LocalDate.of(2024, 4, 1), LocalDate.of(2024, 11, 30), true},
            {"Programa de Extensión en Biología Marina", "EXPERIENCIA", "Trabajos de campo en la costa para estudiantes de biología", "Florianopolis", "UFSC", "Laboratorio de Biología Marina UFSC", "Dr. Ana Paula", 0, "ALTO", "https://biolmarina.ufsc.br/extension", LocalDate.of(2024, 6, 1), LocalDate.of(2024, 12, 15), true},

            //  Florianópolis - CENTRO_HISTORICO (many programs)
            {"Mentoria para Emprendedores", "MENTORIA", "Programa de acompanamiento de emprendedores locales por parte de empresarios exitosos", "Florianopolis", "CENTRO_HISTORICO", "Associacao Comercial de Florianopolis", "Carlos Silva", 1, "MEDIO", "https://acfloripa.org.br/mentoria", LocalDate.of(2024, 2, 1), null, true},
            {"Experiencia de Voluntariado en Bibliotecas", "EXPERIENCIA", "Apoyo a lectores y organizacion de fondos bibliograficos en bibliotecas comunitarias", "Florianopolis", "CENTRO_HISTORICO", "Rede de Bibliotecas de Florianopolis", "Sandra Oliveira", 1, "MEDIO", "https://bibliotecas.floripa.gov.br/voluntariado", LocalDate.of(2024, 3, 1), LocalDate.of(2024, 12, 31), true},
            {"Curso de Historia de Florianópolis", "FORMACION", "Aprender sobre la historia y cultura de la ciudad", "Florianopolis", "CENTRO_HISTORICO", "Museo Histórico de SC", null, 1, "MEDIO", "https://museohistorico.sc.gov.br/curso-historia", LocalDate.of(2024, 4, 1), LocalDate.of(2024, 10, 31), true},
            {"Mentoria en Restauración de Edificios Históricos", "MENTORIA", "Acompañamiento en técnicas de restauración", "Florianopolis", "CENTRO_HISTORICO", "Instituto del Patrimonio Histórico SC", "Arq. Fernanda Lima", 0, "MEDIO", "https://iphsc.org.br/mentoria-restauracion", LocalDate.of(2024, 5, 1), null, true},
            {"Curso de Fotografía Documental", "FORMACION", "Aprender a capturar la historia de la ciudad a través de la fotografía", "Florianopolis", "CENTRO_HISTORICO", "Escuela de Fotografía SC", "Ricardo Mendes", 1, "MEDIO", "https://fotografiasc.org.br/documental", LocalDate.of(2024, 8, 1), LocalDate.of(2025, 2, 15), true},

            //  Florianópolis - CBD_BEIRAMAR (many programs)
            {"Mentoria en Contenido Digital", "MENTORIA", "Acompañamiento en creacion de contenido para redes sociales", "Florianopolis", "CBD_BEIRAMAR", "Agencia de Contenidos Creativos", "Gustavo Santos", 1, "MEDIO", "https://accreativos.com.br/mentoria-contenido", LocalDate.of(2024, 6, 15), null, true},
            {"Curso de Gestion Cultural", "FORMACION", "Administracion de proyectos y espacios culturales para gestores emergentes", "Florianopolis", "CBD_BEIRAMAR", "Fundacion Cultural de Florianopolis Franklin Cascaes", null, 1, "MEDIO", "https://fundacultural.floripa.gov.br/gestion-cultural", LocalDate.of(2024, 8, 1), LocalDate.of(2024, 12, 31), true},
            {"Experiencia en Feria de Economia Solidaria", "EXPERIENCIA", "Organizacion y atencion en ferias de productos artesanales y de economia solidaria", "Florianopolis", "CBD_BEIRAMAR", "Red de Economia Solidaria SC", "Claudia Ferreira", 1, "MEDIO", "https://ecosolidaria-sc.org.br/feria", LocalDate.of(2024, 9, 1), null, true},
            {"Mentoria en Marketing para Pequeños Negocios", "MENTORIA", "Acompañamiento en estrategias de marketing para emprendedores", "Florianopolis", "CBD_BEIRAMAR", "SEBRAE SC", "Maria Oliveira", 1, "ALTO", "https://sebrae.sc.gov.br/marketing-pequenos", LocalDate.of(2024, 7, 1), null, true},

            //  Florianópolis - JURERE (medium programs)
            {"Mentoria en Gestion de Proyectos", "MENTORIA", "Acompañamiento en metodologias agiles y gestion de proyectos", "Florianopolis", "JURERE", "PMI Santa Catarina", "Ricardo Gomes", 1, "MEDIO", "https://pmisc.org.br/mentoria-proyectos", LocalDate.of(2024, 3, 10), null, true},
            {"Curso de Primeros Auxilios", "FORMACION", "Capacitacion basica en primeros auxilios y RCP para la comunidad", "Florianopolis", "JURERE", "Cruz Roja Brasileña - Filial SC", null, 1, "ALTO", "https://cruzroja.org.br/primeros-auxilios-floripa", LocalDate.of(2024, 5, 1), LocalDate.of(2024, 10, 31), true},

            //  Florianópolis - RESIDENCIAL_NORTE (medium programs)
            {"Programa de Formacion en Ingles", "FORMACION", "Curso de ingles para profesionales", "Florianopolis", "RESIDENCIAL_NORTE", "Language Center", null, 1, "ALTO", "https://languagecenter.com.br/ingles", LocalDate.of(2024, 2, 1), LocalDate.of(2024, 9, 30), true},
            {"Mentoria en Economia del Hogar", "MENTORIA", "Acompañamiento en planificacion familiar y ahorro energetico para familias", "Florianopolis", "RESIDENCIAL_NORTE", "Instituto Familia Sustentable", "Rosana Teixeira", 1, "MEDIO", "https://ifamiliasustentavel.org.br/mentoria", LocalDate.of(2024, 6, 1), null, true},

            //  Florianópolis - SC401_CORREDOR (medium programs)
            {"Mentoria en Finanzas Personales", "MENTORIA", "Acompañamiento en gestion de finanzas personales", "Florianopolis", "SC401_CORREDOR", "Instituto de Finanzas Personales", "Paula Ribeiro", 1, "MEDIO", "https://ifp.org.br/mentoria-finanzas", LocalDate.of(2024, 4, 1), null, true},
            {"Curso de Seguridad Vial para Motociclistas", "FORMACION", "Capacitacion en conduccion segura y normativa de transito para motos", "Florianopolis", "SC401_CORREDOR", "DETRAN-SC - Nucleo Florianopolis", null, 1, "ALTO", "https://detran.sc.gov.br/curso-motociclistas", LocalDate.of(2024, 4, 1), LocalDate.of(2024, 10, 31), true},

            //  Florianópolis - VIA_EXPRESSA_CORREDOR (medium programs)
            {"Mentoria para Jovenes Profesionales", "MENTORIA", "Acompañamiento en insercion laboral y desarrollo profesional", "Florianopolis", "VIA_EXPRESSA_CORREDOR", "Fundacion Jovenes Profesionales", "Fernanda Lima", 1, "ALTO", "https://fjp.org.br/mentoria-jovenes", LocalDate.of(2024, 5, 1), null, true},
            {"Curso de Atencion al Cliente y Ventas", "FORMACION", "Tecnicas de ventas, comunicacion y servicio al cliente para comerciantes", "Florianopolis", "VIA_EXPRESSA_CORREDOR", "CDL Florianopolis", null, 1, "MEDIO", "https://cdlflorianopolis.org.br/curso-ventas", LocalDate.of(2024, 6, 10), LocalDate.of(2024, 11, 10), true},

            //  Florianópolis - AEROPORTO_HLZ (medium programs)
            {"Programa de Formacion en IoT", "FORMACION", "Curso de Internet de las Cosas y automatizacion", "Florianopolis", "AEROPORTO_HLZ", "Instituto de Tecnologia Avanzada", null, 0, "ALTO", "https://ita.com.br/iot", LocalDate.of(2024, 6, 1), LocalDate.of(2024, 11, 30), true},
            {"Mentoria en Logistica y Cadena de Suministro", "MENTORIA", "Acompañamiento a profesionales del sector logistico y de transporte", "Florianopolis", "AEROPORTO_HLZ", "ABOL - Asociacion Brasileña de Operadores Logisticos SC", "Sergio Nunes", 1, "MEDIO", "https://abol-sc.org.br/mentoria", LocalDate.of(2024, 7, 1), null, true},

            //  Florianópolis - LAGOA_CONCEICAO (medium programs)
            {"Mentoria en Desarrollo Personal", "MENTORIA", "Acompañamiento en habilidades blandas y crecimiento profesional", "Florianopolis", "LAGOA_CONCEICAO", "Instituto de Desarrollo Humano", "Ana Costa", 1, "MEDIO", "https://idh.org.br/mentoria-personal", LocalDate.of(2024, 2, 15), null, true},
            {"Curso de Kayak y Seguridad Acuática", "FORMACION", "Aprender a navegar en kayak y medidas de seguridad en la laguna", "Florianopolis", "LAGOA_CONCEICAO", "Club Náutico Lagoa Conceição", "Marcos Silva", 1, "MEDIO", "https://clubnauticolagoa.org.br/kayak", LocalDate.of(2024, 9, 1), LocalDate.of(2025, 3, 15), true},

            //  Florianópolis - CAMPECHE (medium programs)
            {"Experiencia en Monitoreo Ambiental Costero", "EXPERIENCIA", "Recoleccion de datos y limpieza de playas con equipos de investigacion", "Florianopolis", "CAMPECHE", "Instituto Oceanografico Sul", "Rafael Duarte", 0, "ALTO", "https://ios.org.br/monitoreo-costero", LocalDate.of(2024, 6, 1), LocalDate.of(2024, 11, 30), true},
            {"Curso de Surf para Principiantes", "FORMACION", "Aprender a surfear con seguridad y respeto por el medio ambiente", "Florianopolis", "CAMPECHE", "Escuela de Surf Campeche", "João Santos", 1, "BAJO", "https://surfcampeche.com.br/principiantes", LocalDate.of(2024, 10, 1), LocalDate.of(2025, 4, 15), true},

            //  Florianópolis - COQUEIROS (medium programs)
            {"Curso de Diseno UX/UI", "FORMACION", "Formacion en diseno de experiencia de usuario", "Florianopolis", "COQUEIROS", "Instituto de Diseno", null, 0, "ALTO", "https://institutodediseno.com.br/ux-ui", LocalDate.of(2024, 4, 15), LocalDate.of(2024, 10, 30), true},
            {"Mentoria en Cocina Saludable", "MENTORIA", "Acompañamiento en técnicas de cocina saludable", "Florianopolis", "COQUEIROS", "Instituto de Nutrición SC", "Dra. Carla Mendes", 1, "MEDIO", "https://nutrisc.org.br/cocina-saludable", LocalDate.of(2024, 5, 15), null, true},

            //  Florianópolis - NORTE_ILHA (new cluster, adding programs)
            {"Curso de Jardinería Urbana", "FORMACION", "Aprender a crear y mantener jardines en espacios pequeños", "Florianopolis", "NORTE_ILHA", "Associacao de Jardineros de Florianopolis", "Luciana Costa", 1, "BAJO", "https://jardinerosfloripa.org.br/urbana", LocalDate.of(2024, 4, 1), LocalDate.of(2024, 10, 15), true},
            {"Experiencia en Mantenimiento de Parques Locales", "EXPERIENCIA", "Voluntariado en el cuidado de parques y áreas verdes", "Florianopolis", "NORTE_ILHA", "Prefeitura de Florianopolis - Secretaria de Medio Ambiente", "Paulo Souza", 1, "MEDIO", "https://floripa.gov.br/meioambiente/voluntarios", LocalDate.of(2024, 3, 1), LocalDate.of(2024, 12, 31), true},

            //  Florianópolis - CANASVIEIRAS (new cluster, adding programs)
            {"Mentoria en Emprendimiento de Food Trucks", "MENTORIA", "Acompañamiento en la creación y gestión de food trucks", "Florianopolis", "CANASVIEIRAS", "Associacao de Food Trucks SC", "André Lima", 1, "MEDIO", "https://foodtruckssc.org.br/mentoria", LocalDate.of(2024, 6, 1), null, true},
            {"Curso de Mantenimiento de Bicicletas", "FORMACION", "Aprender a reparar y mantener bicicletas", "Florianopolis", "CANASVIEIRAS", "Escuela de Ciclistas SC", "Carlos Pereira", 1, "BAJO", "https://ciclistassc.org.br/mantenimiento", LocalDate.of(2024, 5, 1), LocalDate.of(2024, 11, 30), true},

            //  Florianópolis - INGLESES (new cluster, adding programs)
            {"Programa de Formación en Danza Folclórica", "FORMACION", "Aprender danzas folclóricas brasileñas", "Florianopolis", "INGLESES", "Grupo Folclórico Floripa", "Mariana Rocha", 1, "BAJO", "https://folclorofloripa.org.br/cursos", LocalDate.of(2024, 3, 15), LocalDate.of(2024, 9, 15), true},
            {"Mentoria en Organización de Eventos Comunitarios", "MENTORIA", "Acompañamiento en la planificación y ejecución de eventos para la comunidad", "Florianopolis", "INGLESES", "Associacao de Residentes Ingleses", "Fernanda Alves", 1, "MEDIO", "https://residentesingleses.org.br/eventos", LocalDate.of(2024, 4, 1), null, true},

            //  Florianópolis - ESTREITO_CAPOEIRAS (new cluster, adding programs)
            {"Curso de Capoeira para Niños", "FORMACION", "Clases de capoeira para niños de 6 a 12 años", "Florianopolis", "ESTREITO_CAPOEIRAS", "Grupo Capoeira Floripa", "Mestre Zé", 1, "BAJO", "https://capoeirafloripa.org.br/ninos", LocalDate.of(2024, 2, 1), LocalDate.of(2024, 12, 15), true},
            {"Experiencia en Proyecto de Murales Comunitarios", "EXPERIENCIA", "Creación de murales artísticos en las calles del barrio", "Florianopolis", "ESTREITO_CAPOEIRAS", "Colectivo de Artistas Estreito", "Lucia Mendes", 1, "MEDIO", "https://artistasestreito.org.br/murales", LocalDate.of(2024, 5, 1), LocalDate.of(2024, 11, 30), true},

            //  Sao Jose - SAO_JOSE_KOBRASOL (medium programs)
            {"Experiencia de Voluntariado en Salud", "EXPERIENCIA", "Voluntariado en hospitales locales para jovenes", "Sao Jose", "SAO_JOSE_KOBRASOL", "Cruz Roja Brasileña", "Pedro Mendes", 0, "ALTO", "https://cruzroja.org.br/voluntariado-salud", LocalDate.of(2024, 4, 1), LocalDate.of(2024, 11, 30), true},
            {"Curso de Auxiliar de Farmacia", "FORMACION", "Formacion tecnica en atencion farmaceutica y manipulacion de medicamentos", "Sao Jose", "SAO_JOSE_KOBRASOL", "Escuela Tecnica de Saude SC", null, 1, "ALTO", "https://etss.com.br/auxiliar-farmacia", LocalDate.of(2024, 3, 1), LocalDate.of(2024, 9, 30), true},

            //  Sao Jose - SAO_JOSE_CENTRO (medium programs)
            {"Experiencia Comunitaria en Jardinagem", "EXPERIENCIA", "Proyecto de cuidado de espacios publicos con participacion de la comunidad", "Sao Jose", "SAO_JOSE_CENTRO", "ONG Verde Vida", "Maria Souza", 1, "BAJO", "https://verde-vida.org/jardines", LocalDate.of(2024, 3, 1), LocalDate.of(2024, 12, 31), true},
            {"Mentoria en Comunicacion Comunitaria", "MENTORIA", "Acompañamiento a lideres vecinales en comunicacion efectiva y gestion de conflictos", "Sao Jose", "SAO_JOSE_CENTRO", "Instituto Liderazgo Comunitario SC", "Flavia Andrade", 1, "MEDIO", "https://ilcsc.org.br/mentoria-comunicacion", LocalDate.of(2024, 5, 1), null, true},

            //  Sao Jose - SAO_JOSE_ROÇADO (medium programs)
            {"Curso de Construccion Sustentable", "FORMACION", "Tecnicas de construccion con materiales reciclados y bajo impacto ambiental", "Sao Jose", "SAO_JOSE_ROÇADO", "Sinduscon Sao Jose", null, 1, "MEDIO", "https://sinduscon-sj.org.br/construccion-sustentable", LocalDate.of(2024, 6, 1), LocalDate.of(2024, 12, 31), true},
            {"Experiencia en Apoyo a Agricultores Familiares", "EXPERIENCIA", "Ayuda en la venta y distribución de productos agrícolas locales", "Sao Jose", "SAO_JOSE_ROÇADO", "Associacao de Agricultores de Sao Jose", "José Silva", 1, "MEDIO", "https://agricultoressaojose.org.br/apoyo", LocalDate.of(2024, 4, 15), LocalDate.of(2024, 12, 15), true},

            //  Sao Jose - SAO_JOSE_BARREIROS (new cluster, adding programs)
            {"Mentoria en Emprendimiento Rural", "MENTORIA", "Acompañamiento en negocios agrícolas y rurales", "Sao Jose", "SAO_JOSE_BARREIROS", "SEBRAE Sao Jose", "Ana Costa", 1, "ALTO", "https://sebrae.sc.gov.br/saojose/rural", LocalDate.of(2024, 5, 1), null, true},
            {"Curso de Apicultura para Principiantes", "FORMACION", "Aprender a criar abejas y producir miel", "Sao Jose", "SAO_JOSE_BARREIROS", "Associacao de Apicultores SC", "Luiz Pereira", 1, "BAJO", "https://apicultoressc.org.br/principiantes", LocalDate.of(2024, 7, 1), LocalDate.of(2025, 1, 31), true},

            //  Sao Jose - ESTREITO_CAPOEIRAS (new cluster, adding programs)
            {"Curso de Música para Principiantes", "FORMACION", "Clases de guitarra y canto para jóvenes", "Sao Jose", "ESTREITO_CAPOEIRAS", "Escuela de Música Sao Jose", "Carlos Mendes", 1, "BAJO", "https://musicasj.org.br/principiantes", LocalDate.of(2024, 3, 1), LocalDate.of(2024, 9, 15), true},
            {"Experiencia en Club de Lectura Comunitario", "EXPERIENCIA", "Organización y participación en un club de lectura", "Sao Jose", "ESTREITO_CAPOEIRAS", "Biblioteca Pública Sao Jose", "Mariana Souza", 1, "BAJO", "https://bibliotecasj.org.br/clublectura", LocalDate.of(2024, 2, 1), null, true},

            //  Palhoca - PALHOCA_CENTRO (medium programs)
            {"Curso de Agricultura Urbana", "FORMACION", "Aprender a cultivar alimentos en espacios pequeños", "Palhoca", "PALHOCA_CENTRO", "Associacao de Agricultura Urbana de Palhoca", "Marcia Silva", 1, "MEDIO", "https://aupalhoca.org.br/curso-agricultura", LocalDate.of(2024, 4, 1), LocalDate.of(2024, 11, 30), true},
            {"Mentoria en Gestion de Microempresas", "MENTORIA", "Acompañamiento contable, fiscal y de gestion para microempresarios", "Palhoca", "PALHOCA_CENTRO", "Contaje - Consultoria Contable SC", "Roberto Assuncao", 1, "ALTO", "https://contaje.com.br/mentoria-microempresas", LocalDate.of(2024, 5, 1), null, true},

            //  Palhoca - PALHOCA_PEDRA_BRANCA (medium programs)
            {"Curso de Energia Solar Residencial", "FORMACION", "Instalacion y mantenimiento de paneles solares para tecnicoss electricistas", "Palhoca", "PALHOCA_PEDRA_BRANCA", "SENAI Palhoca", null, 1, "ALTO", "https://senai.br/palhoca/energia-solar", LocalDate.of(2024, 6, 1), LocalDate.of(2024, 12, 15), true},
            {"Experiencia en Conservación de Áreas Verdes", "EXPERIENCIA", "Voluntariado en la protección de la naturaleza local", "Palhoca", "PALHOCA_PEDRA_BRANCA", "ONG Conservación Palhoca", "Fernanda Lima", 1, "MEDIO", "https://conservacionpalhoca.org.br/voluntarios", LocalDate.of(2024, 4, 1), LocalDate.of(2024, 12, 31), true},

            //  Palhoca - SAO_JOSE_BARREIROS (new cluster, adding programs)
            {"Curso de Costura y Moda Sostenible", "FORMACION", "Aprender a coser y crear ropa sostenible", "Palhoca", "SAO_JOSE_BARREIROS", "Escuela de Moda Palhoca", "Luciana Alves", 1, "MEDIO", "https://modapalhoca.org.br/sostenible", LocalDate.of(2024, 5, 1), LocalDate.of(2024, 11, 30), true},
            {"Mentoria en Venta de Productos Artesanales", "MENTORIA", "Acompañamiento en la comercialización de artesanías", "Palhoca", "SAO_JOSE_BARREIROS", "Associacao de Artesanos Palhoca", "Maria Pereira", 1, "MEDIO", "https://artesanospalhoca.org.br/venta", LocalDate.of(2024, 6, 1), null, true},

            //  Biguacu - BIGUACU_BR101_NORTE (medium programs)
            {"Curso de Mantenimiento de Motocicletas", "FORMACION", "Aprender a reparar y mantener motos", "Biguacu", "BIGUACU_BR101_NORTE", "Escuela Tecnica de Biguacu", null, 1, "ALTO", "https://etbiguacu.com.br/curso-motos", LocalDate.of(2024, 2, 15), LocalDate.of(2024, 9, 15), true},
            {"Mentoria en Producción de Leche y Derivados", "MENTORIA", "Acompañamiento en la producción de productos lácteos", "Biguacu", "BIGUACU_BR101_NORTE", "Associacion de Productores de Leche SC", "José Oliveira", 1, "MEDIO", "https://lechesc.org.br/mentoria", LocalDate.of(2024, 4, 1), null, true},
            {"Curso de Carpintería Básica", "FORMACION", "Aprender técnicas básicas de carpintería", "Biguacu", "BIGUACU_BR101_NORTE", "Escuela de Carpintería Biguacu", "Carlos Souza", 1, "BAJO", "https://carpinteriabiguacu.org.br/basica", LocalDate.of(2024, 3, 1), LocalDate.of(2024, 9, 30), true}
        };

        List<SocialProgram> all = new ArrayList<>();

        for (Object[] p : programs) {
            String nombre = (String) p[0];
            String tipo = (String) p[1];
            String descripcion = (String) p[2];
            String municipio = (String) p[3];
            String cluster = (String) p[4];
            String organizacion = (String) p[5];
            String liderReferente = (String) p[6];
            Integer replicable = (Integer) p[7];
            String impactoEstimado = (String) p[8];
            String urlReferencia = (String) p[9];
            LocalDate fechaInicio = (LocalDate) p[10];
            LocalDate fechaFin = (LocalDate) p[11];
            Boolean activo = (Boolean) p[12];

            all.add(build(nombre, tipo, descripcion, municipio, cluster, organizacion, liderReferente, replicable, impactoEstimado, urlReferencia, fechaInicio, fechaFin, activo));
        }

        repo.saveAll(all);
    }

    private SocialProgram build(String nombre, String tipo, String descripcion, String municipio, String cluster,
                               String organizacion, String liderReferente, Integer replicable, String impactoEstimado,
                               String urlReferencia, LocalDate fechaInicio, LocalDate fechaFin, Boolean activo) {
        return SocialProgram.builder()
            .nombre(nombre)
            .tipo(tipo)
            .descripcion(descripcion)
            .municipio(municipio)
            .cluster(cluster)
            .organizacion(organizacion)
            .liderReferente(liderReferente)
            .replicable(replicable)
            .impactoEstimado(impactoEstimado)
            .urlReferencia(urlReferencia)
            .fechaInicio(fechaInicio)
            .fechaFin(fechaFin)
            .activo(activo)
            .build();
    }
}
