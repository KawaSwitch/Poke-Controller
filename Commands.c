#include "Commands.h"

// sync controller with Switch
const Command sync[] PROGMEM = {
	{ NOP,      50 },
	{ A,        2 },
	{ NOP,      200 },
	{ HOME,     2 },
	{ NOP,      50 },
	{ A,        2 },
	{ NOP,      50 },
};
const int sync_size = (int)(sizeof(sync) / sizeof(Command));

// unsync controller from Switch
const Command unsync[] PROGMEM = {
	{ NOP,      50 },
	{ HOME,     2 },
	{ NOP,      20 },
	{ DOWN,		5 },
    { NOP, 		2 },
    { RIGHT, 	2 },
    { NOP, 		5 },
    { RIGHT, 	2 },
    { NOP,  	5 },
    { RIGHT,  	2 },
	{ NOP, 		5 },
	{ A,        5 },
    { NOP, 		60 },
	{ A,        2 },
	{ NOP,      30 },
	{ A,        2 },
	{ NOP,      30 },
};
const int unsync_size = (int)(sizeof(unsync) / sizeof(Command));

// Mashing button A
const Command mash_a_commands[] PROGMEM = {
	{ NOP,      20 },
	{ A,        5 },
};
const int mash_a_size = (int)(sizeof(mash_a_commands) / sizeof(Command));

// Mashing button X (for debug)
const Command mash_x_commands[] PROGMEM = {
	{ NOP,      20 },
	{ X,        5 },
};
const int mash_x_size = (int)(sizeof(mash_x_commands) / sizeof(Command));

// Mashing button HOME (for debug)
const Command mash_home_commands[] PROGMEM = {
	{ NOP,      20 },
	{ HOME,        5 },
};
const int mash_home_size = (int)(sizeof(mash_home_commands) / sizeof(Command));

// Auto League
const Command auto_league_commands[] PROGMEM = {
	{ NOP,      20 },
	{ A,        5 },
	{ NOP,      20 },
	{ A,        5 },
	{ NOP,      20 },
	{ A,        5 },
	{ NOP,      20 },
	{ A,        5 },
	{ NOP,      20 },
	{ A,        5 },
	{ NOP,      20 },
	{ A,        5 },
	{ NOP,      20 },
	{ A,        5 },
	{ NOP,      20 },
	{ A,        5 },
	{ NOP,      20 },
	{ A,        5 },
	{ NOP,      20 },
	{ A,        5 },

	{ NOP,      20 },
	{ B,        5 },
};
const int auto_league_size = (int)(sizeof(auto_league_commands) / sizeof(Command));

// infinity watt earning
// from: https://medaka.5ch.net/test/read.cgi/poke/1574816324/ >>25
const Command inf_watt_commands[] PROGMEM = {
    { NOP,  	70 },
	{ A,		2 },
	{ NOP,		50},
	{ B,		2 },
	{ NOP,		50},
	{ B,		2 },
	{ NOP,		50},
	{ B,		2 },
	{ NOP,		50},
	{ B,		2 },
	{ NOP,		50},
	{ B,		2 },
	{ NOP,		50},
	{ A,		2 },
	{ NOP,		50},
	{ A,		2 },
	{ NOP,		175},

	{ HOME,		5},//HOME画面に遷移
	{ NOP,		20},
	{ LEFT,		2},//画面右端に移動
	{ NOP,		8},
	{ DOWN,		2},//スリープに移動
	{ LEFT,		2},//設定に移動
	{ A,		2},//決定
	{ NOP,		45},
	{ DOWN,		2},//画面の明るさに移動
	{ RS_DOWN,	2},//ロックに移動
	{ DOWN,		2},//みまもり設定に移動
	{ RS_DOWN,	2},//インターネットに移動
	{ DOWN,		2},//データ管理に移動
	{ RS_DOWN,	2},//ユーザーに移動
	{ DOWN,		2},//Miiに移動
	{ RS_DOWN,	2},//amiiboに移動
	{ DOWN,		2},//テーマに移動
	{ RS_DOWN,	2},//通知に移動
	{ DOWN,		2},//スリープに移動
	{ RS_DOWN,	2},//コントローラーとセンサーに移動
	{ DOWN,		2},//Bluetoothオーディオに移動
	{ RS_DOWN,	2},//テレビ出力に移動
	{ DOWN,		2},//本体に移動
	{ NOP,		2},
	{ A,		2},//本体の更新に移動
	{ NOP,		15},
	{ DOWN,		2},//ドックの更新に移動
	{ RS_DOWN,	2},//本体のニックネームに移動
	{ DOWN,		25},//言語に移動(画面スクロール)
	{ RS_DOWN,	2},//地域に移動
	{ DOWN,		2},//日付と時刻に移動
	{ A,		2},//決定
	{ NOP,		10},
	{ DOWN,		2},//タイムゾーンに移動
	{ RS_DOWN,	2},//現在の日付と時刻に移動
	{ NOP,		2},
	{ A,		2},//決定
	{ NOP,		10},
	{ RIGHT,	2},//月に移動
	{ RS_RIGHT,	2},//日に移動
	{ UP,		2},//1日進める
	{ RIGHT,	2},//時に移動
	{ RS_RIGHT,	2},//分に移動
	{ RIGHT,	2},//OKに移動
	{ NOP,		2},
	{ A,		2},//決定  
	{ NOP,		20},
	{ HOME,		5},//HOMEに戻る
	{ NOP,		35},
	{ HOME,		5},//ゲームに戻る
	{ NOP,		35},
	{ B,		2},
	{ NOP,		40},
	{ A,		2},
	{ NOP,		100},
};
const int inf_watt_size = (int)(sizeof(inf_watt_commands) / sizeof(Command));

const Command pickupberry_commands[] PROGMEM = {
    { NOP,  	5 },
	{ A,		2 },
	{ NOP,		20},
	{ A,		2 },
	{ NOP,		20},
	{ A,		2 },
	{ NOP,		20},
	{ B,		2 },
	{ NOP,		20},
	{ B,		2 },
	{ NOP,		20},
	{ B,		2 },
	{ NOP,		20},
	{ B,		2 },
	{ NOP,		20},
	{ B,		2 },
	{ NOP,		20},
	{ B,		2 },
	{ NOP,		20},
	{ B,		2 },
	{ NOP,		20},
	{ B,		2 },
	{ NOP,		20},
	{ B,		2 },
	{ NOP,		20},
	{ B,		2 },
	{ NOP,		20},
	{ B,		2 },
	{ NOP,		20},
	{ B,		2 },
	{ NOP,		20},
	{ B,		2 },
	{ NOP,		20},
	{ B,		2 },
	{ NOP,		20},
	{ B,		2 },
	{ NOP,		20},
	{ B,		2 },
	{ NOP,		20},
	{ B,		2 },
	{ NOP,		20},
	{ B,		2 },
	{ NOP,		20},

	{ HOME,		5},//HOME画面に遷移
	{ NOP,		20},
	{ LEFT,		2},//画面右端に移動
	{ NOP,		8},
	{ DOWN,		2},//スリープに移動
	{ LEFT,		2},//設定に移動
	{ A,		2},//決定
	{ NOP,		45},
	{ DOWN,		2},//画面の明るさに移動
	{ RS_DOWN,	2},//ロックに移動
	{ DOWN,		2},//みまもり設定に移動
	{ RS_DOWN,	2},//インターネットに移動
	{ DOWN,		2},//データ管理に移動
	{ RS_DOWN,	2},//ユーザーに移動
	{ DOWN,		2},//Miiに移動
	{ RS_DOWN,	2},//amiiboに移動
	{ DOWN,		2},//テーマに移動
	{ RS_DOWN,	2},//通知に移動
	{ DOWN,		2},//スリープに移動
	{ RS_DOWN,	2},//コントローラーとセンサーに移動
	{ DOWN,		2},//Bluetoothオーディオに移動
	{ RS_DOWN,	2},//テレビ出力に移動
	{ DOWN,		2},//本体に移動
	{ NOP,		2},
	{ A,		2},//本体の更新に移動
	{ NOP,		15},
	{ DOWN,		2},//ドックの更新に移動
	{ RS_DOWN,	2},//本体のニックネームに移動
	{ DOWN,		25},//言語に移動(画面スクロール)
	{ RS_DOWN,	2},//地域に移動
	{ DOWN,		2},//日付と時刻に移動
	{ A,		2},//決定
	{ NOP,		10},
	{ DOWN,		2},//タイムゾーンに移動
	{ RS_DOWN,	2},//現在の日付と時刻に移動
	{ NOP,		2},
	{ A,		2},//決定
	{ NOP,		10},
	{ RIGHT,	2},//月に移動
	{ RS_RIGHT,	2},//日に移動
	{ UP,		2},//1日進める
	{ RIGHT,	2},//時に移動
	{ RS_RIGHT,	2},//分に移動
	{ RIGHT,	2},//OKに移動
	{ NOP,		2},
	{ A,		2},//決定  
	{ NOP,		20},
	{ HOME,		5},//HOMEに戻る
	{ NOP,		35},
	{ HOME,		5},//ゲームに戻る
	{ NOP,		35},
};
const int pickupberry_size = (int)(sizeof(pickupberry_commands) / sizeof(Command));

const Command changetheyear_commands[] PROGMEM = {
	{ NOP,		10},
/* 1年進めるブロック */
	{ LEFT,	2},//分に移動
	{ RS_LEFT,	2},//時に移動
	{ LEFT,	2},//日に移動
	{ RS_LEFT,	2},//月に移動
	{ LEFT,	2},//年に移動
	{ UP,		2},//1年進める
	{ RIGHT,	2},//月に移動
	{ RS_RIGHT,	2},//日に移動
	{ RIGHT,	2},//時に移動
	{ RS_RIGHT,	2},//分に移動
	{ RIGHT,	2},//OKに移動
	{ NOP,		2},
	{ A,		2},//決定  
	{ NOP,		4},
	{ A,		2},//決定  
	{ NOP,		4},
/* 2000年まで戻るブロック */
	{ LEFT,	2},//分に移動
	{ RS_LEFT,	2},//時に移動
	{ LEFT,	2},//日に移動
	{ RS_LEFT,	2},//月に移動
	{ LEFT,	2},//年に移動
	{ DOWN,		230},//2000年に戻す
	{ RIGHT,	2},//月に移動
	{ RS_RIGHT,	2},//日に移動
	{ RIGHT,	2},//時に移動
	{ RS_RIGHT,	2},//分に移動
	{ RIGHT,	2},//OKに移動
	{ NOP,		2},
	{ A,		2},//決定  
	{ NOP,		4},
	{ A,		2},//決定  
	{ NOP,		4},
/* 消費終了後のブロック */
	{ B,		2},
	{ NOP,		20},
	{ UP,		2},//HOMEに戻る
	{ NOP,		4},
	{ A,		5},//ゲームに戻る
	{ NOP,		4},
/* 日付変更する前にメニュー画面にしてもらうこと前提にコメントアウト */
//	{ X,		5},//乱数消費を避けるため、メニューに入る
//	{ NOP,		35}
};
const int changetheyear_size = (int)(sizeof(changetheyear_commands) / sizeof(Command));
