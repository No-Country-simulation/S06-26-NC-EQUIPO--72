package com.example.appbitb2g.seed;

import java.math.BigDecimal;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Component;

import com.example.appbitb2g.model.Antenna;
import com.example.appbitb2g.repository.AntenaRepository;
import com.example.appbitb2g.repository.SocialProgramRepository;

@Component
@Profile("dev-mock-csv")
public class AntenasSeeder {
    @Autowired
    private AntenaRepository repo;

    public void seed() {
        if (repo.count() > 0)
            return;

        repo.saveAll(List.of(
                new Antenna("724050683790307", "SC401_CORREDOR", "Florianopolis", new BigDecimal("-27.5865"),
                        new BigDecimal("-48.4968")),
                new Antenna("724050683793381", "ESTREITO_CAPOEIRAS", "Florianopolis", new BigDecimal("-27.599258"),
                        new BigDecimal("-48.579861")),
                new Antenna("724050683793438", "NORTE_ILHA", "Florianopolis", new BigDecimal("-27.482269"),
                        new BigDecimal("-48.491897")),
                new Antenna("724050683884425", "ESTREITO_CAPOEIRAS", "Florianopolis", new BigDecimal("-27.601483"),
                        new BigDecimal("-48.592317")),
                new Antenna("724050683898841", "TRINDADE", "Florianopolis", new BigDecimal("-27.594028"),
                        new BigDecimal("-48.520928")),
                new Antenna("724050683935003", "UFSC", "Florianopolis", new BigDecimal("-27.594397"),
                        new BigDecimal("-48.556111")),
                new Antenna("724050683935135", "CANASVIEIRAS", "Florianopolis", new BigDecimal("-27.4292"),
                        new BigDecimal("-48.458697")),
                new Antenna("724050683935372", "AEROPORTO_HLZ", "Florianopolis", new BigDecimal("-27.7"),
                        new BigDecimal("-48.550647")),
                new Antenna("724050683983270", "CBD_BEIRAMAR", "Florianopolis", new BigDecimal("-27.591528"),
                        new BigDecimal("-48.552775")),
                new Antenna("724050684142457", "CBD_BEIRAMAR", "Florianopolis", new BigDecimal("-27.585"),
                        new BigDecimal("-48.544722")),
                new Antenna("724050684142570", "RESIDENCIAL_NORTE", "Florianopolis", new BigDecimal("-27.529258"),
                        new BigDecimal("-48.514072")),
                new Antenna("724050684142660", "SAO_JOSE_KOBRASOL", "Sao Jose", new BigDecimal("-27.6075"),
                        new BigDecimal("-48.638889")),
                new Antenna("724050684144778", "CBD_BEIRAMAR", "Florianopolis", new BigDecimal("-27.595694"),
                        new BigDecimal("-48.548194")),
                new Antenna("724050684145073", "CBD_BEIRAMAR", "Florianopolis", new BigDecimal("-27.587967"),
                        new BigDecimal("-48.555231")),
                new Antenna("724050684145529", "LAGOA_CONCEICAO", "Florianopolis", new BigDecimal("-27.6044"),
                        new BigDecimal("-48.4752")),
                new Antenna("724050684641810", "SC401_CORREDOR", "Florianopolis", new BigDecimal("-27.568425"),
                        new BigDecimal("-48.513053")),
                new Antenna("724050684641828", "CAMPECHE", "Florianopolis", new BigDecimal("-27.656481"),
                        new BigDecimal("-48.509303")),
                new Antenna("724050684641844", "NORTE_ILHA", "Florianopolis", new BigDecimal("-27.451714"),
                        new BigDecimal("-48.452175")),
                new Antenna("724050684646269", "SAO_JOSE_CENTRO", "Sao Jose", new BigDecimal("-27.608008"),
                        new BigDecimal("-48.62685")),
                new Antenna("724050685014142", "ESTREITO_CAPOEIRAS", "Florianopolis", new BigDecimal("-27.605047"),
                        new BigDecimal("-48.594306")),
                new Antenna("724050685015130", "PALHOCA_PEDRA_BRANCA", "Palhoca", new BigDecimal("-27.622639"),
                        new BigDecimal("-48.674258")),
                new Antenna("724050685015378", "SAO_JOSE_ROÇADO", "Sao Jose", new BigDecimal("-27.567222"),
                        new BigDecimal("-48.617175")),
                new Antenna("724050685015394", "SAO_JOSE_KOBRASOL", "Sao Jose", new BigDecimal("-27.586064"),
                        new BigDecimal("-48.609675")),
                new Antenna("724050687263808", "INGLESES", "Florianopolis", new BigDecimal("-27.439722"),
                        new BigDecimal("-48.387592")),
                new Antenna("724050688192491", "SAO_JOSE_ROÇADO", "Sao Jose", new BigDecimal("-27.570694"),
                        new BigDecimal("-48.644742")),
                new Antenna("724050696233975", "PALHOCA_PEDRA_BRANCA", "Palhoca", new BigDecimal("-27.641511"),
                        new BigDecimal("-48.7061")),
                new Antenna("724050696483882", "LAGOA_CONCEICAO", "Florianopolis", new BigDecimal("-27.599642"),
                        new BigDecimal("-48.468531")),
                new Antenna("724050696484153", "TRINDADE", "Florianopolis", new BigDecimal("-27.612097"),
                        new BigDecimal("-48.543378")),
                new Antenna("724050696484161", "ESTREITO_CAPOEIRAS", "Florianopolis", new BigDecimal("-27.598331"),
                        new BigDecimal("-48.576389")),
                new Antenna("724050696484269", "AEROPORTO_HLZ", "Florianopolis", new BigDecimal("-27.664203"),
                        new BigDecimal("-48.534994")),
                new Antenna("724050696484277", "CAMPECHE", "Florianopolis", new BigDecimal("-27.682578"),
                        new BigDecimal("-48.491986")),
                new Antenna("724050696484293", "CANASVIEIRAS", "Florianopolis", new BigDecimal("-27.434297"),
                        new BigDecimal("-48.460603")),
                new Antenna("724050696484315", "INGLESES", "Florianopolis", new BigDecimal("-27.43975"),
                        new BigDecimal("-48.419811")),
                new Antenna("724050696484323", "NORTE_ILHA", "Florianopolis", new BigDecimal("-27.497669"),
                        new BigDecimal("-48.419811")),
                new Antenna("724050697326900", "VIA_EXPRESSA_CORREDOR", "Florianopolis", new BigDecimal("-27.612839"),
                        new BigDecimal("-48.593017")),
                new Antenna("724050697341860", "ESTREITO_CAPOEIRAS", "Florianopolis", new BigDecimal("-27.596094"),
                        new BigDecimal("-48.599653")),
                new Antenna("724050697341879", "RESIDENCIAL_NORTE", "Florianopolis", new BigDecimal("-27.542733"),
                        new BigDecimal("-48.505306")),
                new Antenna("724050697342190", "CBD_BEIRAMAR", "Florianopolis", new BigDecimal("-27.5834"),
                        new BigDecimal("-48.544683")),
                new Antenna("724050697342212", "RESIDENCIAL_NORTE", "Florianopolis", new BigDecimal("-27.528831"),
                        new BigDecimal("-48.513689"))));

    }

}
