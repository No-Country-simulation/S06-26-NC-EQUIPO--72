package com.example.appbitb2g.seed;

import com.example.appbitb2g.model.FluxoVias;
import com.example.appbitb2g.repository.FluxoViasRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
@Profile("dev")
public class FluxoViasSeeder {

    @Autowired
    private FluxoViasRepository fluxoViasRepository;

    public void seed(){
        if (fluxoViasRepository.count()>0)
            return; // Evita duplicar datos si ta existen en la base de datos

        fluxoViasRepository.saveAll(List.of(
                new FluxoVias(null, "724050697342190", "724050697605965", "CBD_BEIRAMAR", "CBD_BEIRAMAR", 1535, 1606, 1.025, "MANHA", 4.9),
                new FluxoVias(null, "724050697605965", "724050684142457", "CBD_BEIRAMAR", "CBD_BEIRAMAR", 1465, 1507, 1.065, "MANHA", 4.6),
                new FluxoVias(null, "724050684142457", "724050683983270", "CBD_BEIRAMAR", "CBD_BEIRAMAR", 1495, 1542, 1.076, "MANHA", 4.7),
                new FluxoVias(null, "7240501005162597", "7240501005162724", "LAGOA_CONCEICAO", "CAMPECHE", 182, 183, 11.898, "MANHA", 0.7),
                new FluxoVias(null, "7240501005162724", "7240501004550410", "CAMPECHE", "UFSC", 203, 204, 9.072, "MANHA", 0.7),
                new FluxoVias(null, "7240501004550410", "724050697342190", "UFSC", "CBD_BEIRAMAR", 194, 195, 1.461, "MANHA", 0.7),
                new FluxoVias(null, "7240501003962715", "7240501005162724", "BIGUACU_BR101_NORTE", "CAMPECHE", 182, 184, 22.196, "MANHA", 0.7),
                new FluxoVias(null, "7240501005162724", "724050699925231", "CAMPECHE", "SAO_JOSE_KOBRASOL", 193, 196, 15.406, "MANHA", 0.7),
                new FluxoVias(null, "724050699925231", "7240501003495238", "SAO_JOSE_KOBRASOL", "TRINDADE", 175, 176, 12.091, "MANHA", 0.6)
        ));


    }
}
