using System;
using Game;

public static class RandomizerBonus
{
	public static void UpgradeID(int ID)
	{
		switch (ID)
		{
		case 0:
			Characters.Sein.Mortality.Health.SetAmount((float)(Characters.Sein.Mortality.Health.MaxHealth + 20));
			Randomizer.showHint("Mega Health");
			break;
		case 1:
			Characters.Sein.Energy.SetCurrent(Characters.Sein.Energy.Max + 5f);
			Randomizer.showHint("Mega Energy");
			break;
		case 6:
			Randomizer.showHint("Spirit Flame Damage Upgrade");
			break;
		case 8:
			Randomizer.showHint("Split Flame Upgrade");
			break;
		case 10:
			Randomizer.showHint("Grenade Power Upgrade");
			break;
		case 12:
			Randomizer.showHint("Health Efficiency");
			break;
		case 13:
			Randomizer.showHint("Energy Efficiency");
			break;
		case 14:
			Randomizer.showHint("Spirit Light Efficiency");
			break;
		case 15:
			Randomizer.showHint("Spirit Link Heal Upgrade");
			break;
		case 16:
			Randomizer.showHint("Charge Flame Efficiency");
			break;
		case 17:
			Randomizer.showHint("Extra Air Dash");
			break;
		case 18:
			Randomizer.showHint("Charge Dash Efficiency");
			break;
		case 19:
			Randomizer.showHint("Extra Double Jump");
			break;
		case 20:
			Randomizer.showHint("Health Regeneration");
			break;
		case 22:
			Randomizer.showHint("Energy Regeneration");
			break;
		}
		if (ID > 1)
		{
			Characters.Sein.Inventory.SkillPointsCollected += 1 << ID;
		}
	}

	public static int SpiritFlameStrength()
	{
		return ((Characters.Sein.Inventory.SkillPointsCollected & 0x000000c0) >> 6) * 2;
	}

	public static int SpiritFlameTargets()
	{
        int value = (Characters.Sein.Inventory.SkillPointsCollected & 0x00000300) >> 8;
        if (value == 3)
        {
            return 4;
        }
        return value;
	}

	public static float GrenadePower()
	{
		return (float)((Characters.Sein.Inventory.SkillPointsCollected & 0x00000c00) >> 10) * 5f;
	}

	public static bool HealthEfficiency()
	{
		return (Characters.Sein.Inventory.SkillPointsCollected & 0x00001000) >> 12 == 1;
	}

	public static bool EnergyEfficiency()
	{
		return (Characters.Sein.Inventory.SkillPointsCollected & 0x00002000) >> 13 == 1;
	}

	public static bool ExpEfficiency()
	{
		return (Characters.Sein.Inventory.SkillPointsCollected & 0x00004000) >> 14 == 1;
	}

	public static bool SoulLinkHeal()
	{
		return (Characters.Sein.Inventory.SkillPointsCollected & 0x00008000) >> 15 == 1;
	}

	public static bool ChargeFlameEfficiency()
	{
		return (Characters.Sein.Inventory.SkillPointsCollected & 0x00010000) >> 16 == 1;
	}

	public static bool DoubleAirDash()
	{
		return (Characters.Sein.Inventory.SkillPointsCollected & 0x00020000) >> 17 == 1;
	}
    
    public static bool DoubleAirDashUsed = false;

	public static bool ChargeDashEfficiency()
	{
		return (Characters.Sein.Inventory.SkillPointsCollected & 0x00040000) >> 18 == 1;
	}

	public static bool DoubleJumpUpgrade()
	{
		return (Characters.Sein.Inventory.SkillPointsCollected & 0x00080000) >> 19 == 1;
	}

	public static int HealthRegeneration()
	{
		return (Characters.Sein.Inventory.SkillPointsCollected & 0x00300000) >> 20;
	}

	public static int EnergyRegeneration()
	{
		return (Characters.Sein.Inventory.SkillPointsCollected & 0x00c00000) >> 22;
	}
}