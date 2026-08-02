package com.example.appbitb2g.enums;

import lombok.Getter;

@Getter
public enum ServiceType {
	SALUD_MENTAL("SALUD_MENTAL"),
	MENTORIA("MENTORIA"),
	EXPERIENCIA("EXPERIENCIA"),
	FORMACION("FORMACION"),
	EMPLEO("EMPLEO"),
	EDUCACION("EDUCACION");

	private final String value;

	ServiceType(String value) {
		this.value = value;
	}

	public static ServiceType fromString(String text) {
		if (text == null) return null;
		for (ServiceType b : ServiceType.values()) {
			if (b.value.equalsIgnoreCase(text)) {
				return b;
			}
		}
		return null;
	}
}
