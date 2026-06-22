package com.example.appbitb2g.seed;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.context.annotation.Profile;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

@Component
@Profile("dev")
@Order(1)
public class DatabaseSeeder implements ApplicationRunner {

    @Autowired private SocialProgramSeeder socialProgramSeeder;
    @Autowired private TerritorialIndicatorsSeeder territorialIndicatorsSeeder;
    @Autowired private AntenasSeeder antenasSeeder;
    @Autowired private AssinantesSeeder assinantesSeeder;
    @Autowired private ConcentracaoSeeder concentracaoSeeder;
    @Autowired private FluxoViasSeeder fluxoViasSeeder;
    @Autowired private AggregateMobilitySeeder aggregateMobilitySeeder;

    @Override
    public void run(ApplicationArguments args) {
        socialProgramSeeder.seed();
        territorialIndicatorsSeeder.seed();
        antenasSeeder.seed();
        assinantesSeeder.seed();
        concentracaoSeeder.seed();
        fluxoViasSeeder.seed();
        aggregateMobilitySeeder.seed();
    }
}