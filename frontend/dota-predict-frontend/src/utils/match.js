export function generateDraftBarData(rawData) {
  let {
    radiant_picks, radiant_bans,
    dire_picks, dire_bans,
  } = rawData

  // Add loadings
  radiant_picks = radiant_picks.map(value => value === 0 ? -1 : value);
  dire_picks = dire_picks.map(value => value === 0 ? -1 : value);

  return {
    radiantPicks: radiant_picks,
    radiantBans: radiant_bans,
    direPicks: dire_picks,
    direBans: dire_bans,
    radiantWinChance: rawData.radiant_win_chance * 100,
    radiantTeam: rawData.radiant_team,
    direTeam: rawData.dire_team,
  }
}
